'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSignIn, useSession } from 'better-auth/react';
import { TextField, Flex, Button, Heading, Text } from '@radix-ui/themes';
import { EyeOpenIcon, EyeClosedIcon } from '@radix-ui/react-icons';

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
  const { data: session, isPending: sessionPending } = useSession();
  const { signIn, isPending: signInPending } = useSignIn({
    onSuccess: () => {
      // Redirect to dashboard after successful login
      router.push('/dashboard');
    },
    onError: (error) => {
      console.error('Login error:', error);
    }
  });

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

    try {
      await signIn({
        email: formData.email,
        password: formData.password
      });
    } catch (error) {
      console.error('Login failed:', error);
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
              <TextField.Root>
                <TextField.Input
                  aria-label="Email address"
                  placeholder="Email address"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  disabled={isPending}
                  aria-invalid={!!errors.email}
                  aria-describedby={errors.email ? "email-error" : undefined}
                />
              </TextField.Root>
              {errors.email && (
                <Text id="email-error" color="red" size="2" role="alert">{errors.email}</Text>
              )}

              {/* Password Field */}
              <TextField.Root>
                <TextField.Slot>
                  <TextField.Icon
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOpenIcon /> : <EyeClosedIcon />}
                  </TextField.Icon>
                </TextField.Slot>
                <TextField.Input
                  aria-label="Password"
                  placeholder="Password"
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  disabled={isPending}
                  aria-invalid={!!errors.password}
                  aria-describedby={errors.password ? "password-error" : undefined}
                />
              </TextField.Root>
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
                disabled={isPending}
                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                aria-busy={isPending}
              >
                {isPending ? 'Signing In...' : 'Sign In'}
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