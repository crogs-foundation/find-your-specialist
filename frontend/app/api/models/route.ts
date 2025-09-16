import axios from "axios";

export async function GET() {
    try {

        const response = await axios.get(`${process.env.API_URL}/models`);
        return new Response(JSON.stringify(response.data), { status: 200 })
    } catch (reason) {
        const message =
            reason instanceof Error ? reason.message : 'Unexpected error'

        return new Response(message, { status: 500 })
    }
}
