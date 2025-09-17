import { NextRequest } from 'next/server';


export async function GET(request: NextRequest) {
    const params = request.nextUrl.searchParams;

    const response = await fetch(
        `${process.env.API_URL}/chat?prompt=${params.get("prompt")}&model=${params.get("model")}&specialist=${params.get("specialist")}`,
    );

    if (!response.ok || !response.body) {
        let errorText = undefined;
        try {
            errorText = (await response.json()).detail;
        } catch {
            // Ignore parsing errors
        }
        return new Response(errorText || "Failed to connect to backend or response body is missing.", {
            status: 500,
            headers: {
                'Content-Type': 'text/plain'
            }
        });
    }

    return new Response(response.body, {
        headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }
    });
}