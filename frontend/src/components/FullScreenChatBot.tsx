'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import ChatBot from './ChatBot';

export default function FullScreenChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated } = useAuth();

  // Show for authenticated users, but also show when dev bypass is enabled
  const DEV_BYPASS_ENABLED = typeof window !== 'undefined' && localStorage.getItem('DEV_CHATBOT_BYPASS') === 'true';

  // Handle fullscreen toggle
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Close chat when pressing Escape key
  useEffect(() => {
    const handleEscKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleEscKey);
    return () => window.removeEventListener('keydown', handleEscKey);
  }, [isOpen]);

  // Determine if chat should be shown
  const shouldShowChat = isAuthenticated || DEV_BYPASS_ENABLED;

  if (!shouldShowChat) {
    return null;
  }

  return (
    <>
      {/* Floating Button to Open Full Screen Chat */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center justify-center text-white z-50"
          aria-label="Open full screen chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}

      {/* Full Screen Chat Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 bg-white flex flex-col">
          {/* Header with close button */}
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-4 flex justify-between items-center">
            <h2 className="text-white text-xl font-semibold">AI Task Assistant</h2>
            <button
              onClick={toggleChat}
              className="text-white hover:text-gray-200 transition-colors"
              aria-label="Close chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>

          {/* ChatBot Component taking full space */}
          <div className="flex-1 overflow-hidden bg-white">
            <ChatBot className="h-full w-full" />
          </div>
        </div>
      )}
    </>
  );
}