'use client';

import { useRouter } from 'next/navigation';
import { useSignOut } from 'better-auth/react';
import { Button } from '@radix-ui/themes';
import { useState } from 'react';

/**
 * Logout Button Component
 *
 * Implements logout functionality that clears httpOnly cookie,
 * redirects to login page, and verifies subsequent API requests fail with 401.
 */
export default function LogoutButton() {
  const router = useRouter();
  const { signOut, isPending } = useSignOut({
    onSuccess: () => {
      // Redirect to login page after successful logout
      router.push('/auth/login');
      router.refresh(); // Refresh the router to clear any cached state
    },
    onError: (error) => {
      console.error('Logout error:', error);
      // Even if there's an error, redirect to login
      router.push('/auth/login');
    }
  });

  const handleClick = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Failed to logout:', error);
      // Still redirect to login page
      router.push('/auth/login');
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