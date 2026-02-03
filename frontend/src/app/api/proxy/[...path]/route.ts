import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

/**
 * API Proxy Route Handler
 *
 * This proxy enables the frontend to send authenticated requests to the FastAPI backend.
 * It reads the JWT token from httpOnly cookies (which JavaScript cannot access) and
 * forwards it to the backend in the Authorization header.
 *
 * Flow:
 * 1. Frontend calls /api/proxy/api/user123/tasks
 * 2. Proxy reads better-auth.session_token from httpOnly cookie
 * 3. Proxy forwards to backend with Authorization: Bearer <token>
 * 4. Backend verifies JWT and returns response
 * 5. Proxy returns response to frontend
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  return handleProxyRequest(request, await params, "GET");
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  return handleProxyRequest(request, await params, "POST");
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  return handleProxyRequest(request, await params, "PUT");
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  return handleProxyRequest(request, await params, "DELETE");
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  return handleProxyRequest(request, await params, "PATCH");
}

async function handleProxyRequest(
  request: NextRequest,
  params: { path: string[] },
  method: string
) {
  try {
    // Construct backend URL from path segments
    const path = params.path.join("/");
    const backendUrl = `${BACKEND_URL}/${path}`;

    // Get session token from httpOnly cookie
    const cookieStore = await cookies();
    const sessionToken = cookieStore.get("better-auth.session_token");

    if (!sessionToken) {
      return NextResponse.json(
        { detail: "Not authenticated. Please log in." },
        { status: 401 }
      );
    }

    // Prepare request headers
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${sessionToken.value}`,
    };

    // Prepare request options
    const options: RequestInit = {
      method,
      headers,
    };

    // Include request body for POST, PUT, PATCH
    if (["POST", "PUT", "PATCH"].includes(method)) {
      const body = await request.json().catch(() => null);
      if (body) {
        options.body = JSON.stringify(body);
      }
    }

    // Forward request to backend
    const response = await fetch(backendUrl, options);

    // Handle non-JSON responses (like 204 No Content)
    if (response.status === 204) {
      return new NextResponse(null, { status: 204 });
    }

    // Parse response
    const data = await response.json().catch(() => ({ detail: "Invalid response from server" }));

    // Return response with same status code
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Proxy error:", error);
    return NextResponse.json(
      { detail: "Proxy request failed. Please try again." },
      { status: 500 }
    );
  }
}
