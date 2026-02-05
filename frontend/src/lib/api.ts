// API client for the Todo application
// This will handle all API calls and automatically attach JWT tokens

class ApiClient {
  constructor() {
    // Constructor intentionally left empty
    // Token will be retrieved dynamically from localStorage when needed
  }

  // Method to get the current token from localStorage
  private getToken(): string {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token') || '';
    }
    return '';
  }

  setToken(token: string) {
    // Store in localStorage for persistence
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    }
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${process.env.NEXT_PUBLIC_API_BASE_URL}${endpoint}`;
    const currentToken = this.getToken();

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (currentToken) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${currentToken}`;
    }

    const config: RequestInit = {
      headers,
      ...options,
    };

    const response = await fetch(url, config);

    // Handle authentication errors specifically
    if (response.status === 401) {
      // Clear token and user data from localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('user');

      // Clear token from this instance
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
      }

      throw new Error(`Authentication failed: ${response.status} ${response.statusText}`);
    }

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    // For DELETE requests, don't try to parse JSON if response is 204 No Content
    if (config.method === 'DELETE' && response.status === 204) {
      return {};
    }

    // For DELETE requests that return 200, check if there's content to parse
    if (config.method === 'DELETE' && response.status === 200) {
      const contentLength = response.headers.get('content-length');
      if (contentLength === '0' || !response.body) {
        return {};
      }
    }

    return response.json();
  }

  // Task-related API methods
  async getTasks(status?: 'all' | 'pending' | 'completed', sort?: 'created' | 'title', order?: 'asc' | 'desc') {
    let url = `${process.env.NEXT_PUBLIC_API_BASE_URL}/tasks`;
    const params = new URLSearchParams();
    const currentToken = this.getToken();

    if (status) params.append('status', status);
    if (sort) params.append('sort', sort);
    if (order) params.append('order', order);

    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${currentToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get tasks: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async createTask(title: string, description?: string) {
    const currentToken = this.getToken();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`,
      },
      body: JSON.stringify({ title, description }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getTask(id: number) {
    const currentToken = this.getToken();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/tasks/${id}`, {
      headers: {
        'Authorization': `Bearer ${currentToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get task: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async updateTask(id: number, title?: string, description?: string, completed?: boolean) {
    const currentToken = this.getToken();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`,
      },
      body: JSON.stringify({ title, description, completed }),
    });

    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async deleteTask(id: number) {
    const currentToken = this.getToken();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/tasks/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${currentToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async toggleTaskCompletion(id: number) {
    const currentToken = this.getToken();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/tasks/${id}/complete`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle task completion: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async chat(message: string, conversationId?: string) {
    const currentToken = this.getToken();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`,
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId || null
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to send chat message: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }
}

export const apiClient = new ApiClient();
