'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Flex, Container, Text, Button } from '@radix-ui/themes';
import LogoutButton from '@/components/auth/logout-button';
import { authClient } from '@/lib/auth-client';

/**
 * Protected Dashboard Layout
 *
 * This layout wraps all dashboard pages and ensures that only authenticated
 * users can access them. If a user is not authenticated, they are redirected
 * to the login page.
 */
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { data: session, isPending } = authClient.useSession();

  useEffect(() => {
    // If session is loaded and user is not authenticated, redirect to login
    if (!isPending && !session?.user) {
      router.push('/auth/login');
    }
  }, [session, isPending, router]);

  // Show loading state while checking session
  if (isPending) {
    return (
      <Flex direction="column" align="center" justify="center" className="min-h-screen">
        <Text>Loading...</Text>
      </Flex>
    );
  }

  // If user is not authenticated, don't render the layout
  if (!session?.user) {
    return null; // Redirect effect happens in useEffect
  }

  return (
    <Flex direction="column" className="min-h-screen">
      {/* Navigation Bar */}
      <nav className="bg-gray-800 text-white py-4 px-6 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold">Todo App</h1>
        </div>

        <Flex gap="4" align="center">
          <a href="/dashboard" className="hover:underline">Dashboard</a>
          <a href="/dashboard/tasks" className="hover:underline">Tasks</a>

          {/* User Profile Dropdown */}
          <div className="relative">
            <Button variant="soft">
              {session.user.name || session.user.email}
            </Button>

            {/* Simple dropdown menu */}
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 hidden group-hover:block z-10">
              <a href="/dashboard/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
              <a href="/dashboard/settings" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
              <LogoutButton />
            </div>
          </div>
        </Flex>
      </nav>

      {/* Main Content */}
      <Container size="3" className="py-6 flex-grow">
        {children}
      </Container>

      {/* Footer */}
      <footer className="bg-gray-100 py-4 px-6 text-center text-sm text-gray-500">
        <Text>© {new Date().getFullYear()} Todo App. All rights reserved.</Text>
      </footer>
    </Flex>
  );
}