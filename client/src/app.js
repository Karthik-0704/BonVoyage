import { Routes, Route } from "react-router-dom";
import WelcomePage from "./pages/welcome";
import LoginPage from "./pages/login";
import SignupPage from "./pages/signup";
import HomePage from "./pages/home";
import TripPage from "./pages/trip";

function App() {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/user/:userId" element={<HomePage />} />
      <Route path="/trip/:tripIndex" element={<TripPage />} />
    </Routes>
  );
}

export default App;