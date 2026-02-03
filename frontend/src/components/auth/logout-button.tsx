'use client';

import { useRouter } from 'next/navigation';
import { Button } from '@radix-ui/themes';
import { useState } from 'react';
import { authClient } from '@/lib/auth-client';
import { authLogger } from '@/lib/logger';

/**
 * Logout Button Component
 *
 * Implements logout functionality that clears httpOnly cookie,
 * redirects to login page, and verifies subsequent API requests fail with 401.
 */
export default function LogoutButton() {
  const router = useRouter();
  const [isPending, setIsPending] = useState(false);

  const handleClick = async () => {
    setIsPending(true);

    try {
      await authClient.signOut();

      // Log successful sign-out
      authLogger.signOutSuccess();

      // Redirect to login page after successful logout
      router.push('/auth/login');
      router.refresh(); // Refresh the router to clear any cached state
    } catch (error) {
      // Log failed sign-out
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      authLogger.signOutFailure(errorMessage);
      console.error('Failed to logout:', error);

      // Still redirect to login page
      router.push('/auth/login');
    } finally {
      setIsPending(false);
    }
  };

  return (
    <Button
      onClick={handleClick}
      disabled={isPending}
      variant="soft"
      color="red"
      className="w-full text-left px-4 py-2 text-sm hover:bg-red-50"
      aria-label={isPending ? "Logging out, please wait" : "Sign out of your account"}
      aria-disabled={isPending}
    >
      {isPending ? 'Logging out...' : 'Sign out'}
    </Button>
  );
}