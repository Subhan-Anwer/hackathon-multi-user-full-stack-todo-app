import { betterAuth } from "better-auth";
import { Pool } from "@neondatabase/serverless";

// Create database connection pool
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export const auth = betterAuth({
  database: {
    provider: "pg",
    connection: pool,
  },

  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },

  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    updateAge: 60 * 60 * 24, // Update every 24 hours
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7, // 7 days
    },
  },

  advanced: {
    cookiePrefix: "better-auth",
    defaultCookieAttributes: {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 24 * 7, // 7 days
    },
  },

  secret: process.env.BETTER_AUTH_SECRET!,
});
