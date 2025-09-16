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
        }
        catch {

        }

        return new Response(errorText || "Failed to connect to backend or response body is missing.", { status: 500 });
    }

    return new Response(response.body as ReadableStream<Uint8Array>)
}
