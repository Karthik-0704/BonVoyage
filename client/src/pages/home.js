import { useState } from "react";
import { useLocation } from "react-router-dom";
import Sidebar from "../components/sidebar";
import TripInput from "../components/trip_input";

function HomePage() {
    const location = useLocation();
    const state = location.state || {};
    const user_id = state.user_id || 1;
    const name = state.name || "User";
    const email = state.email || "";

    const [lastTrip, setLastTrip] = useState(null);

    return (
        <div style={{ display: "flex", minHeight: "100vh" }}>
            <Sidebar userId={user_id} name={name} email={email} />
            <main style={{ flex: 1, padding: "1rem" }}>
                <h1>Welcome, {name}</h1>
                <TripInput
                    userId={user_id}
                    onTripPlanned={(trip) => setLastTrip(trip)}
                />

                {lastTrip && (
                    <section>
                        <h2>Planned trip details</h2>

                        <h3>Summary</h3>
                        <p>
                            <strong>
                                {lastTrip.source} → {lastTrip.destination}
                            </strong>
                        </p>
                        <p>
                            {lastTrip.days} days, {lastTrip.people_count} people, budget ${lastTrip.budget}
                        </p>

                        {lastTrip.flights && lastTrip.flights.length > 0 && (
                            <>
                                <h3>Flights</h3>
                                <ul>
                                    {lastTrip.flights.map((f, i) => (
                                        <li key={i}>
                                            {f.airline} via {f.provider} - ${f.price} ({f.duration_hours}h)
                                        </li>
                                    ))}
                                </ul>
                            </>
                        )}

                        {lastTrip.hotels && lastTrip.hotels.length > 0 && (
                            <>
                                <h3>Hotels</h3>
                                <ul>
                                    {lastTrip.hotels.map((h, i) => (
                                        <li key={i}>
                                            {h.name} via {h.provider} - ${h.price_per_day}/night ({h.rating}★)
                                        </li>
                                    ))}
                                </ul>
                            </>
                        )}

                        {lastTrip.itinerary && lastTrip.itinerary.length > 0 && (
                            <>
                                <h3>Itinerary</h3>
                                <ul>
                                    {lastTrip.itinerary.map((item, i) => (
                                        <li key={i}>
                                            Day {item.day}: {item.plan}
                                        </li>
                                    ))}
                                </ul>
                            </>
                        )}

                        <h3>Raw plan JSON</h3>
                        <pre>{JSON.stringify(lastTrip, null, 2)}</pre>
                    </section>
                )}
            </main>
        </div>
    );
}

export default HomePage;