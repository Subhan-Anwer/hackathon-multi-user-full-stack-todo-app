import { auth } from './auth';

/**
 * Session Check Utility
 *
 * Reads current session via `/api/auth/session` to determine authentication status.
 */
export async function checkSession() {
  try {
    const response = await fetch('/api/auth/session', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.status === 401 || response.status === 403) {
      // Token is expired or invalid, redirect to login
      redirectToLogin();
      return null;
    }

    if (response.ok) {
      const data = await response.json();
      return data.session || null;
    }

    return null;
  } catch (error) {
    console.error('Error checking session:', error);
    // If there's an error checking session, assume it's invalid
    redirectToLogin();
    return null;
  }
}

/**
 * Handle expired/invalid JWT tokens
 * Detect on protected route access, clear cookie, redirect to `/login`
 */
export async function handleExpiredToken() {
  try {
    // Clear any local session data
    localStorage.clear();
    sessionStorage.clear();

    // Attempt to logout from backend to clear server-side session
    await fetch('/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    }).catch(() => {
      // Ignore errors during logout
    });

    // Redirect to login with specific message about expired session
    const redirectUrl = `/auth/login?message=${encodeURIComponent('Your session has expired. Please log in again.')}`;
    window.location.href = redirectUrl;
  } catch (error) {
    console.error('Error handling expired token:', error);
    // Fallback redirect
    const redirectUrl = `/auth/login?message=${encodeURIComponent('Your session has expired. Please log in again.')}`;
    window.location.href = redirectUrl;
  }
}

/**
 * Check if user is authenticated
 */
export async function isAuthenticated() {
  const session = await checkSession();
  return !!session?.user;
}

/**
 * Redirect to login page
 */
export function redirectToLogin(returnUrl?: string) {
  const redirectUrl = returnUrl
    ? `/auth/login?return=${encodeURIComponent(returnUrl)}`
    : '/auth/login';
  window.location.href = redirectUrl;
}

/**
 * Get current user info
 */
export async function getCurrentUser() {
  const session = await checkSession();
  return session?.user || null;
}