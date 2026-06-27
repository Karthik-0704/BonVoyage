import { useState } from "react";
import API_URL from "../config";

function TripInput({ userId, onTripPlanned }) {
	const [prompt, setPrompt] = useState("");
	const [loading, setLoading] = useState(false);

	async function handleSubmit(e) {
		e.preventDefault();
		if (!userId) {
			alert("Missing user id");
			return;
		}

		setLoading(true);
		try {
			const res = await fetch(`${API_URL}/plan_trip?user_id=${userId}`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ prompt }),
			});

			if (!res.ok) {
				alert("Failed to plan trip");
				return;
			}

			const data = await res.json();

			if (data.error) {
				alert(`Error: ${data.error}`);
				return;
			}

			if (onTripPlanned) {
				onTripPlanned(data);
			}

			setPrompt("");
		} finally {
			setLoading(false);
		}
	}

	return (
		<form onSubmit={handleSubmit}>
			<h2>Plan a new trip</h2>
			<input
				type="text"
				value={prompt}
				onChange={(e) => setPrompt(e.target.value)}
				placeholder="e.g. Fly from New York to Tokyo for 7 days, 2 people, $4000 budget"
				style={{ width: "100%" }}
			/>
			<button type="submit" disabled={loading || !prompt.trim()}>
				{loading ? "Planning..." : "Plan trip"}
			</button>
		</form>
	);
}

export default TripInput;

