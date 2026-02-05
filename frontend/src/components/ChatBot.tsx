import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/lib/auth';
import { apiClient } from '@/lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatProps {
  className?: string;
}

const ChatBot: React.FC<ChatProps> = ({ className }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { token, isAuthenticated, logout } = useAuth();

  // Load conversation history when component mounts
  useEffect(() => {
    loadConversationHistory();
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversationHistory = async () => {
    // For now, we'll just initialize with a welcome message
    // In a real implementation, we would load the most recent conversation
    setMessages([
      {
        id: '1',
        role: 'assistant',
        content: 'Hello! I\'m your AI assistant. You can ask me to manage your tasks using natural language. Try saying "Add task: Buy groceries" or "Show my tasks".',
        timestamp: new Date(),
      }
    ]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || !canUseChatbot) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setIsError(false); // Reset error state when submitting

    try {
      // Call the chat API using the apiClient
      const data = await apiClient.chat(inputValue.trim(), currentConversationId || undefined);

      const aiMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.data.response,
        timestamp: new Date(data.data.timestamp),
      };

      setMessages(prev => [...prev, aiMessage]);

      // Update conversation ID if a new one was created
      if (data.data.conversation_id && !currentConversationId) {
        setCurrentConversationId(data.data.conversation_id);
      }
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Check if it's an authentication error
      if (error.message.includes('401') || error.message.toLowerCase().includes('unauthorized')) {
        setIsError(true);
        setErrorMessage('Authentication error. Please log in again.');

        // Logout the user to reset the session
        logout();

        const errorMessageResponse: Message = {
          id: Date.now().toString(),
          role: 'assistant',
          content: 'Authentication error. Please log in again to continue using the chatbot.',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessageResponse]);
      } else {
        setIsError(true);
        setErrorMessage(error.message || 'Connection error');

        const errorMessageResponse: Message = {
          id: Date.now().toString(),
          role: 'assistant',
          content: `Sorry, I encountered an error connecting to the server: ${error.message || 'Please try again.'}`,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessageResponse]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const quickActions = [
    { text: "Add task: ", example: "Buy groceries" },
    { text: "Show my tasks", example: "" },
    { text: "Complete task: ", example: "Buy groceries" },
    { text: "Delete task: ", example: "Unwanted task" },
  ];

  const handleQuickAction = (action: string) => {
    setInputValue(action);
  };

  // Temporary dev/test bypass for testing chatbot functionality without auth
  const DEV_BYPASS_ENABLED = typeof window !== 'undefined' && localStorage.getItem('DEV_CHATBOT_BYPASS') === 'true';
  const canUseChatbot = token && isAuthenticated || DEV_BYPASS_ENABLED;

  // Toggle for development bypass
  const toggleDevBypass = () => {
    if (DEV_BYPASS_ENABLED) {
      localStorage.removeItem('DEV_CHATBOT_BYPASS');
      alert('Development bypass disabled. Normal authentication required.');
    } else {
      localStorage.setItem('DEV_CHATBOT_BYPASS', 'true');
      alert('Development bypass enabled. Chatbot can be used without authentication for testing.');
    }
    // Force a re-render by updating state
    setInputValue(inputValue + ' '); // Minor state change to trigger re-render
    setTimeout(() => setInputValue(inputValue), 0);
  };

  return (
    <div className={`flex flex-col h-full bg-white rounded-lg shadow-md overflow-hidden ${className}`}>
      {/* Chat Header */}
      <div className="bg-blue-600 text-white p-3 sm:p-4 md:p-4">
        <h2 className="text-lg sm:text-xl md:text-xl font-semibold">AI Task Assistant</h2>
        <p className="text-xs sm:text-sm opacity-80">Manage your tasks with natural language</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-3 sm:p-4 space-y-3 max-h-[calc(100vh-250px)] sm:max-h-[calc(100vh-280px)] md:max-h-[calc(100vh-300px)] lg:max-h-[calc(100vh-320px)]">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[90%] sm:max-w-[85%] md:max-w-[80%] rounded-lg p-2 sm:p-3 ${
                message.role === 'user'
                  ? 'bg-blue-100 text-gray-800 rounded-br-none'
                  : 'bg-gray-100 text-gray-800 rounded-bl-none'
              }`}
            >
              <div className="whitespace-pre-wrap text-sm sm:text-base">{message.content}</div>
              <div
                className={`text-xs sm:text-sm ${
                  message.role === 'user' ? 'text-right text-gray-500' : 'text-left text-gray-500'
                }`}
              >
                {formatTime(message.timestamp)}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 rounded-lg p-2 sm:p-3 rounded-bl-none max-w-[90%] sm:max-w-[85%] md:max-w-[80%]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="border-t bg-gray-50 p-3 sm:p-4">
        <div className="flex flex-wrap gap-2">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => handleQuickAction(action.text + (action.example ? action.example : ""))}
              disabled={isLoading || !canUseChatbot}
              className="text-xs sm:text-sm bg-white border border-blue-200 text-blue-600 rounded-full px-3 py-1.5 hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {action.text}{action.example && <span className="text-gray-500 italic"> {action.example}</span>}
            </button>
          ))}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t p-3 sm:p-4">
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2" noValidate>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={(!canUseChatbot) ? "Please log in to use the chatbot" : "Type your message here..."}
            disabled={isLoading || !canUseChatbot}
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 sm:px-4 sm:py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 cursor-text"
            autoComplete="off"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim() || !canUseChatbot}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer self-end sm:self-auto"
          >
            Send
          </button>
        </form>
        {!token && (
          <div className="mt-2 text-xs sm:text-sm text-yellow-600">
            You must be logged in to use the chatbot. Please log in to your account first.
          </div>
        )}
        <div className="mt-2 text-xs sm:text-sm text-gray-500">
          Example: "Add task: Buy groceries", "Show my tasks", "Complete task: Buy groceries"
        </div>

        {/* Dev/Test Bypass and Session Controls */}
        <div className="mt-3 flex flex-wrap gap-2 text-xs sm:text-sm">
          {DEV_BYPASS_ENABLED && (
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded">
              Dev bypass active
            </span>
          )}
          <button
            onClick={toggleDevBypass}
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-2 py-1 rounded text-xs sm:text-sm"
          >
            {DEV_BYPASS_ENABLED ? 'Disable Dev Bypass' : 'Enable Dev Bypass'}
          </button>
          <button
            onClick={logout}
            className="bg-orange-100 hover:bg-orange-200 text-orange-800 px-2 py-1 rounded text-xs sm:text-sm"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Error Notification - Positioned inline to avoid interfering with input area */}
      {isError && (
        <div className="mx-3 sm:mx-4 mb-3 sm:mb-4 bg-red-50 border-l-4 border-red-500 p-3 sm:p-4 rounded-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">
                <span className="font-medium">Error:</span> {errorMessage}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBot;