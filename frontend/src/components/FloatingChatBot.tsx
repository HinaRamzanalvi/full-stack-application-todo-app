'use client';

import { useState } from 'react';
import { useAuth } from '@/lib/auth';
import ChatBot from './ChatBot';

export default function FloatingChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated } = useAuth();

  // Show for authenticated users, but also show when dev bypass is enabled
  const DEV_BYPASS_ENABLED = typeof window !== 'undefined' && localStorage.getItem('DEV_CHATBOT_BYPASS') === 'true';
  if (!isAuthenticated && !DEV_BYPASS_ENABLED) {
    return null; // Don't show floating chatbot if not authenticated
  }

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="w-full h-screen md:h-[70vh] lg:h-[65vh] xl:h-[60vh] max-w-full md:max-w-md lg:max-w-lg xl:max-w-xl bg-white rounded-none md:rounded-xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-3 flex justify-between items-center">
            <h3 className="text-white font-semibold text-sm md:text-base">AI Assistant</h3>
            <button
              onClick={toggleChat}
              className="text-white hover:text-gray-200 transition-colors"
              aria-label="Close chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
          <div className="flex-1 overflow-hidden">
            <ChatBot className="h-full w-full" />
          </div>
        </div>
      ) : (
        <button
          onClick={toggleChat}
          className="w-14 h-14 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center justify-center text-white"
          aria-label="Open chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}
    </div>
  );
}