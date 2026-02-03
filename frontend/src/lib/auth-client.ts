import { createAuthClient } from 'better-auth/react';

/**
 * Better Auth Client Configuration
 *
 * This is the central authentication client used throughout the application.
 * It provides methods for:
 * - Sign in: authClient.signIn.email({ email, password })
 * - Sign up: authClient.signUp.email({ email, password, name })
 * - Sign out: authClient.signOut()
 * - Session: authClient.useSession() hook
 *
 * @see https://www.better-auth.com/docs/concepts/client
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
});
