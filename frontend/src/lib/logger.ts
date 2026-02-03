/**
 * Authentication Logger for Frontend
 *
 * Provides structured JSON logging for authentication events.
 * All logs are written to console in development mode.
 * In production, these could be sent to a logging service.
 */

interface AuthLogEvent {
  timestamp: string;
  event: string;
  userId?: string;
  email?: string;
  success: boolean;
  error?: string;
  metadata?: Record<string, unknown>;
}

class AuthLogger {
  private isDevelopment = process.env.NODE_ENV === 'development';

  /**
   * Log a structured authentication event
   */
  private logEvent(event: AuthLogEvent): void {
    const logEntry = {
      ...event,
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV,
    };

    if (this.isDevelopment) {
      console.log(JSON.stringify(logEntry, null, 2));
    } else {
      // In production, send to logging service (e.g., DataDog, Sentry)
      console.log(JSON.stringify(logEntry));
    }
  }

  /**
   * Log a sign-in attempt (before API call)
   */
  signInAttempt(email: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signin_attempt',
      email,
      success: false, // Attempt, not success yet
    });
  }

  /**
   * Log successful sign-in
   */
  signInSuccess(userId: string, email: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signin_success',
      userId,
      email,
      success: true,
    });
  }

  /**
   * Log failed sign-in
   */
  signInFailure(email: string, error: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signin_failure',
      email,
      success: false,
      error,
    });
  }

  /**
   * Log a sign-up attempt (before API call)
   */
  signUpAttempt(email: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signup_attempt',
      email,
      success: false,
    });
  }

  /**
   * Log successful sign-up
   */
  signUpSuccess(userId: string, email: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signup_success',
      userId,
      email,
      success: true,
    });
  }

  /**
   * Log failed sign-up
   */
  signUpFailure(email: string, error: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signup_failure',
      email,
      success: false,
      error,
    });
  }

  /**
   * Log successful sign-out
   */
  signOutSuccess(userId?: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signout_success',
      userId,
      success: true,
    });
  }

  /**
   * Log failed sign-out
   */
  signOutFailure(error: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'signout_failure',
      success: false,
      error,
    });
  }

  /**
   * Log session check (when protected routes verify authentication)
   */
  sessionCheck(isAuthenticated: boolean, userId?: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'session_check',
      userId,
      success: isAuthenticated,
      metadata: {
        authenticated: isAuthenticated,
      },
    });
  }

  /**
   * Log session expiry detection
   */
  sessionExpired(userId?: string): void {
    this.logEvent({
      timestamp: new Date().toISOString(),
      event: 'session_expired',
      userId,
      success: false,
      metadata: {
        reason: 'token_expired',
      },
    });
  }
}

export const authLogger = new AuthLogger();
