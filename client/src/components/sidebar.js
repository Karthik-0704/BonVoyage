import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API_URL from "../config";

function Sidebar({ userId, name, email }) {
    const [trips, setTrips] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        async function fetchTrips() {
            try {
                setLoading(true);
                setError(null);
                const res = await fetch(
                    `${API_URL}/get_trips_of_one_user?user_id=${userId}`
                );
                if (!res.ok) {
                    throw new Error("Failed to load trips");
                }
                const data = await res.json();
                setTrips(data);
            } catch (err) {
                setError(err.message || "Something went wrong");
            } finally {
                setLoading(false);
            }
        }

        if (userId) {
            fetchTrips();
        }
    }, [userId]);

    return (
        <aside>
            <h2>Profile</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>

            <hr />

            <h3>Your Trips</h3>
            {loading && <p>Loading trips...</p>}
            {error && <p>{error}</p>}
            {!loading && !error && trips.length === 0 && (<p>No trips planned yet.</p>)}
            <ul>
                {trips.map((trip, index) => (
                    <li
                        key={index}
                        onClick={() =>
                            navigate(`/trip/${index}`, {
                                state: { trip },
                            })
                        }
                    >
                        <div>
                            <strong>
                                {trip.source} → {trip.destination}
                            </strong>
                        </div>
                        <div>{trip.days} days, {trip.people_count} people</div>
                        <div>Budget: ${trip.budget}</div>
                    </li>
                ))}
            </ul>
        </aside>
    );
}

export default Sidebar;

