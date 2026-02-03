'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { TextField, Flex, Button, Heading, Text } from '@radix-ui/themes';
import { EyeOpenIcon, EyeClosedIcon } from '@radix-ui/react-icons';
import { authClient } from '@/lib/auth-client';
import { authLogger } from '@/lib/logger';

/**
 * Login Page Component
 *
 * Implements user authentication with email and password using Better Auth.
 * Features:
 * - Email and password validation
 * - Loading states
 * - Error handling
 * - Password visibility toggle
 * - Forgot password link
 * - Redirect logic: if user already authenticated, redirect to `/dashboard`
 */
export default function LoginPage() {
  const router = useRouter();
  const { data: session, isPending: sessionPending } = authClient.useSession();
  const [signInPending, setSignInPending] = useState(false);

  // Redirect authenticated users away from login page
  useEffect(() => {
    if (!sessionPending && session?.user) {
      // Check for return URL in query params
      const urlParams = new URLSearchParams(window.location.search);
      const returnUrl = urlParams.get('return');

      if (returnUrl) {
        router.push(decodeURIComponent(returnUrl));
      } else {
        router.push('/dashboard');
      }
    }
  }, [session, sessionPending, router]);

  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setSignInPending(true);

    // Log sign-in attempt
    authLogger.signInAttempt(formData.email);

    try {
      const result = await authClient.signIn.email({
        email: formData.email,
        password: formData.password
      });

      // Log successful sign-in - result from signIn.email contains user info
      // Type-safe approach to handle Better Auth response
      if (result && typeof result === 'object') {
        // Safely access user data
        const user = ('user' in result && result.user) ? result.user : null;
        const userId = (user && typeof user === 'object' && 'id' in user && user.id) ? user.id as string : "";
        authLogger.signInSuccess(userId, formData.email);
      } else {
        // Fallback: log without user ID if result structure is unexpected
        authLogger.signInSuccess("", formData.email);
      }

      // Redirect to dashboard after successful login
      router.push('/dashboard');
    } catch (error) {
      // Log failed sign-in
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      authLogger.signInFailure(formData.email, errorMessage);
      console.error('Login failed:', error);
    } finally {
      setSignInPending(false);
    }
  };

  return (
    <Flex
      role="main"
      direction="column"
      align="center"
      justify="center"
      className="min-h-screen bg-gray-50 px-4 py-12 sm:px-6 lg:px-8"
    >
      <Flex
        direction="column"
        gap="5"
        className="w-full max-w-md space-y-8"
      >
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <Heading as="h2" size="6" align="center" aria-level={1}>
            Sign in to your account
          </Heading>
          <Text as="p" color="gray" mt="2" align="center">
            Enter your credentials to access your Todo app
          </Text>
        </div>

        <Flex
          asChild
          direction="column"
          gap="4"
          onSubmit={handleSubmit}
          className="mt-8 sm:mx-auto sm:w-full sm:max-w-sm"
        >
          <form aria-label="Sign in form">
            <Flex direction="column" gap="4">
              {/* Email Field */}
              <div className="space-y-2">
                <input
                  aria-label="Email address"
                  placeholder="Email address"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  disabled={signInPending}
                  aria-invalid={!!errors.email}
                  aria-describedby={errors.email ? "email-error" : undefined}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
                {errors.email && (
                  <Text id="email-error" color="red" size="2" role="alert">{errors.email}</Text>
                )}
              </div>

              {/* Password Field */}
              <div className="space-y-2">
                <div className="relative">
                  <input
                    aria-label="Password"
                    placeholder="Password"
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    disabled={signInPending}
                    aria-invalid={!!errors.password}
                    aria-describedby={errors.password ? "password-error" : undefined}
                    className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    {showPassword ? <EyeOpenIcon /> : <EyeClosedIcon />}
                  </button>
                </div>
                {errors.password && (
                  <Text id="password-error" color="red" size="2" role="alert">{errors.password}</Text>
                )}
              </div>
              {errors.password && (
                <Text id="password-error" color="red" size="2" role="alert">{errors.password}</Text>
              )}

              {/* Forgot Password Link */}
              <Flex justify="end">
                <a
                  href="/auth/forgot-password"
                  className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                  aria-label="Forgot password"
                >
                  Forgot password?
                </a>
              </Flex>

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={signInPending}
                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                aria-busy={signInPending}
              >
                {signInPending ? 'Signing In...' : 'Sign In'}
              </Button>
            </Flex>
          </form>
        </Flex>

        {/* Signup Link */}
        <Flex justify="center">
          <Text as="p" size="2">
            Don't have an account?{' '}
            <a
              href="/auth/signup"
              className="font-medium text-indigo-600 hover:text-indigo-500"
              aria-label="Sign up for a new account"
            >
              Sign up
            </a>
          </Text>
        </Flex>
      </Flex>
    </Flex>
  );
}