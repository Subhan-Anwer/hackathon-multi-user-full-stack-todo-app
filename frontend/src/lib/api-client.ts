/**
 * API Client for Frontend-Backend Communication
 *
 * This client routes all requests through the /api/proxy endpoint,
 * which handles JWT token extraction from httpOnly cookies and
 * forwards requests to the FastAPI backend.
 *
 * Usage:
 *   const tasks = await api.get('/api/user123/tasks');
 *   const task = await api.post('/api/user123/tasks', { title: 'New task' });
 */

interface RequestOptions extends RequestInit {
  body?: any;
}

class APIClient {
  private baseUrl: string;

  constructor() {
    // All requests go through the Next.js API proxy
    this.baseUrl = "/api/proxy";
  }

  /**
   * Make a request through the proxy
   */
  private async request<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const config: RequestInit = {
      ...options,
      credentials: "include", // CRITICAL: Include cookies in request
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    };

    // Stringify body if it's an object
    if (options.body && typeof options.body === "object") {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);

      // Handle 401 Unauthorized - expired/invalid token
      if (response.status === 401) {
        // Redirect to login with session expired message
        window.location.href = `/auth/login?message=${encodeURIComponent('Your session has expired. Please log in again.')}`;
        return undefined as T;
      }

      // Handle 204 No Content
      if (response.status === 204) {
        return undefined as T;
      }

      // Parse JSON response
      const data = await response.json().catch(() => ({}));

      // Handle error responses
      if (!response.ok) {
        const error = new Error(
          data.detail || `HTTP ${response.status}: ${response.statusText}`
        );
        (error as any).status = response.status;
        (error as any).data = data;
        throw error;
      }

      return data as T;
    } catch (error) {
      // Handle network errors or other issues
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error - could be due to expired session
        window.location.href = `/auth/login?message=${encodeURIComponent('Session error. Please log in again.')}`;
      }
      // Re-throw for caller to handle
      throw error;
    }
  }

  /**
   * GET request
   */
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "GET" });
  }

  /**
   * POST request
   */
  async post<T>(endpoint: string, body?: any): Promise<T> {
    return this.request<T>(endpoint, { method: "POST", body });
  }

  /**
   * PUT request
   */
  async put<T>(endpoint: string, body?: any): Promise<T> {
    return this.request<T>(endpoint, { method: "PUT", body });
  }

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "DELETE" });
  }

  /**
   * PATCH request
   */
  async patch<T>(endpoint: string, body?: any): Promise<T> {
    return this.request<T>(endpoint, { method: "PATCH", body });
  }
}

// Export singleton instance
export const api = new APIClient();

// Type definitions for task API responses
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
}

export interface UpdateTaskInput {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Convenience functions for task operations
export const taskAPI = {
  /**
   * Get all tasks for a user
   */
  getTasks: (userId: string) =>
    api.get<Task[]>(`/api/${userId}/tasks`),

  /**
   * Get a specific task by ID
   */
  getTask: (userId: string, taskId: number) =>
    api.get<Task>(`/api/${userId}/tasks/${taskId}`),

  /**
   * Create a new task
   */
  createTask: (userId: string, data: CreateTaskInput) =>
    api.post<Task>(`/api/${userId}/tasks`, data),

  /**
   * Update a task
   */
  updateTask: (userId: string, taskId: number, data: UpdateTaskInput) =>
    api.put<Task>(`/api/${userId}/tasks/${taskId}`, data),

  /**
   * Delete a task
   */
  deleteTask: (userId: string, taskId: number) =>
    api.delete<void>(`/api/${userId}/tasks/${taskId}`),

  /**
   * Toggle task completion status
   */
  toggleComplete: (userId: string, taskId: number) =>
    api.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`),
};
