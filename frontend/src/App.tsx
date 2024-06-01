import { Routes, Route } from "react-router-dom";
import StartScreen from "./pages/StartScreen";
import Game from "./pages/PlayerScreen";
import HostGame from "./pages/GameScreen";
import React, { useEffect, useState } from "react";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<StartScreen />} />
        <Route path="game" element={<Game />} />
        <Route path="HostGame" element={<HostGame />} />
      </Routes>
    </div>
  );
}

export default App;
