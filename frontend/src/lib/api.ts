// API client for the Todo application
// This will handle all API calls and automatically attach JWT tokens

class ApiClient {
  private baseUrl: string;
  private token: string = '';

  constructor() {
    this.baseUrl = process.env.NODE_ENV === 'production'
      ? ''
      : process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
    // Load token from localStorage on initialization
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        this.token = storedToken;
      }
    }
  }

  setToken(token: string) {
    this.token = token;
    // Also store in localStorage for persistence
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    }
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${this.token}`;
    }

    const config: RequestInit = {
      headers,
      ...options,
    };

    const response = await fetch(url, config);

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
    let url = '/tasks';
    const params = new URLSearchParams();

    if (status) params.append('status', status);
    if (sort) params.append('sort', sort);
    if (order) params.append('order', order);

    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    return this.request(url);
  }

  async createTask(title: string, description?: string) {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
  }

  async getTask(id: number) {
    return this.request(`/tasks/${id}`);
  }

  async updateTask(id: number, title?: string, description?: string, completed?: boolean) {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ title, description, completed }),
    });
  }

  async deleteTask(id: number) {
    return this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: number) {
    return this.request(`/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }
}

export const apiClient = new ApiClient();
