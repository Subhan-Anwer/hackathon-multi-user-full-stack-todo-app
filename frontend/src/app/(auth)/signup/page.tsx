'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useRegister, useSession } from 'better-auth/react';
import { TextField, Flex, Button, Heading, Text } from '@radix-ui/themes';
import { EyeOpenIcon, EyeClosedIcon } from '@radix-ui/react-icons';

/**
 * Signup Page Component
 *
 * Implements user registration with email and password using Better Auth.
 * Features:
 * - Email and password validation
 * - Password confirmation
 * - Loading states
 * - Error handling
 * - Password visibility toggle
 * - Redirect logic: if user already authenticated, redirect to `/dashboard`
 */
export default function SignupPage() {
  const router = useRouter();
  const { data: session, isPending: sessionPending } = useSession();
  const { register, isPending: registerPending } = useRegister({
    onSuccess: () => {
      // Redirect to dashboard after successful signup
      router.push('/dashboard');
    },
    onError: (error) => {
      console.error('Signup error:', error);
    }
  });

  // Redirect authenticated users away from signup page
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
    password: '',
    confirmPassword: ''
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
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
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
      await register({
        email: formData.email,
        password: formData.password,
        name: formData.email.split('@')[0] // Use email prefix as name
      });
    } catch (error) {
      console.error('Registration failed:', error);
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
            Create your account
          </Heading>
          <Text as="p" color="gray" mt="2" align="center">
            Sign up for a new Todo app account
          </Text>
        </div>

        <Flex
          asChild
          direction="column"
          gap="4"
          onSubmit={handleSubmit}
          className="mt-8 sm:mx-auto sm:w-full sm:max-w-sm"
        >
          <form aria-label="Sign up form">
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
                  <TextField.Icon aria-label={showPassword ? "Hide password" : "Show password"}>
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
              <Text color="gray" size="1">
                Password must be at least 8 characters
              </Text>

              {/* Confirm Password Field */}
              <TextField.Root>
                <TextField.Slot>
                  <TextField.Icon
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Hide confirm password" : "Show confirm password"}
                  >
                    {showPassword ? <EyeOpenIcon /> : <EyeClosedIcon />}
                  </TextField.Icon>
                </TextField.Slot>
                <TextField.Input
                  aria-label="Confirm Password"
                  placeholder="Confirm Password"
                  type={showPassword ? "text" : "password"}
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                  disabled={isPending}
                  aria-invalid={!!errors.confirmPassword}
                  aria-describedby={errors.confirmPassword ? "confirm-password-error" : undefined}
                />
              </TextField.Root>
              {errors.confirmPassword && (
                <Text id="confirm-password-error" color="red" size="2" role="alert">{errors.confirmPassword}</Text>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={isPending}
                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                aria-busy={isPending}
              >
                {isPending ? 'Creating Account...' : 'Sign Up'}
              </Button>
            </Flex>
          </form>
        </Flex>

        {/* Login Link */}
        <Flex justify="center">
          <Text as="p" size="2">
            Already have an account?{' '}
            <a
              href="/auth/login"
              className="font-medium text-indigo-600 hover:text-indigo-500"
              aria-label="Sign in to your account"
            >
              Sign in
            </a>
          </Text>
        </Flex>
      </Flex>
    </Flex>
  );
}