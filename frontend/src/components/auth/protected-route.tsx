'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'better-auth/react';
import { Flex, Text } from '@radix-ui/themes';

/**
 * Protected Route Wrapper Component
 *
 * Checks session and redirects to `/login` if not authenticated.
 */
export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [checked, setChecked] = useState(false);
  const [showMessage, setShowMessage] = useState(false);

  useEffect(() => {
    if (!isPending) {
      if (!session?.user) {
        // Redirect to login if not authenticated
        const returnUrl = window.location.pathname + window.location.search;
        router.push(`/auth/login?return=${encodeURIComponent(returnUrl)}`);
        setShowMessage(true);
      } else {
        setChecked(true);
      }
    }
  }, [session, isPending, router]);

  // Show loading while checking session
  if (isPending || !checked) {
    if (showMessage) {
      return (
        <Flex direction="column" align="center" justify="center" className="min-h-screen">
          <Text>Please log in to continue</Text>
        </Flex>
      );
    }

    return (
      <Flex direction="column" align="center" justify="center" className="min-h-screen">
        <Text>Loading...</Text>
      </Flex>
    );
  }

  // Render children if authenticated
  return <>{children}</>;
}