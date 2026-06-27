import { useLocation, useParams } from "react-router-dom";

function TripPage() {
  const { tripIndex } = useParams();
  const location = useLocation();
  const { trip } = location.state || {};

  if (!trip) {
    return <p>No trip data found. Try navigating from the sidebar.</p>;
  }

  return (
    <div>
      <h1>
        Trip #{tripIndex}: {trip.source} → {trip.destination}
      </h1>

      <p>
        {trip.days} days, {trip.people_count} people, budget ${trip.budget}
      </p>

      {trip.flights && trip.flights.length > 0 && (
        <>
          <h2>Flights</h2>
          <ul>
            {trip.flights.map((f, i) => (
              <li key={i}>
                {f.airline} via {f.provider} - ${f.price} ({f.duration_hours}h)
              </li>
            ))}
          </ul>
        </>
      )}

      {trip.hotels && trip.hotels.length > 0 && (
        <>
          <h2>Hotels</h2>
          <ul>
            {trip.hotels.map((h, i) => (
              <li key={i}>
                {h.name} via {h.provider} - ${h.price_per_day}/night ({h.rating}★)
              </li>
            ))}
          </ul>
        </>
      )}

      {trip.itinerary && trip.itinerary.length > 0 && (
        <>
          <h2>Itinerary</h2>
          <ul>
            {trip.itinerary.map((item, i) => (
              <li key={i}>
                Day {item.day}: {item.plan}
              </li>
            ))}
          </ul>
        </>
      )}

      <h2>Raw plan JSON</h2>
      <pre>{JSON.stringify(trip, null, 2)}</pre>
    </div>
  );
}

export default TripPage;