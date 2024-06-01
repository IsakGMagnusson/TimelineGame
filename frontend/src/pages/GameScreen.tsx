// Importing modules
import { useState, useEffect } from "react";
import "../App.css";

import JoinedList from "../components/JoinedList";
import InputSettingsDisplay from "../components/InputSettingsDisplay";
import React from "react";
import WinScreen from "./WinScreen";
import TimeLine from "../components/Timeline/TimeLine";
import { socket } from "../Socket";
import PlayerNameBox from "../components/PlayerNameBox";

function HostGame() {
  const [gameCode, setGameCode] = useState<string>("");
  const [joinedPlayers, setJoinedPlayers] = useState([]);
  const [isGameStarted, setIsGameStarted] = useState<boolean>(false);

  const [activePlayerName, setActivePlayerName] = useState<string>("");
  const [winnerName, setWinnerName] = useState<string>("");

  const [disconnectedPlayers, setDisconnectedPlayers] = useState<string[]>([]);

  useEffect(() => {
    socket.connect();
    socket.emit("create_game");
  }, []);

  useEffect(() => {
    function onCreateGameEvent(data: any) {
      setGameCode(data.gamecode);
    }

    function setJoined(data: any) {
      setJoinedPlayers(data.joinedPlayerNames);
    }

    function inform_disconnect(data: any) {
      setDisconnectedPlayers(data.disconnected_players);
    }

    function game_start_host(data: any) {
      setIsGameStarted(data.is_game_started);
      setActivePlayerName(data.active_player_name);
    }

    function new_turn(data: any) {
      setActivePlayerName(data.active_player_name);
    }

    function player_won(data: any) {
      setWinnerName(data.winner_name);
    }

    socket.on("create_game", onCreateGameEvent);
    socket.on("users", setJoined);
    socket.on("inform_disconnect", inform_disconnect);
    socket.on("game_start_host", game_start_host);
    socket.on("new_turn", new_turn);
    socket.on("player_won", player_won);

    return () => {
      socket.off("create_game", onCreateGameEvent);
      socket.off("users", setJoined);
      socket.off("inform_disconnect", inform_disconnect);
      socket.off("game_start_host", game_start_host);
      socket.off("new_turn", new_turn);
      socket.off("player_won", player_won);
    };
  }, [gameCode]);

  socket.on("disconnect", (reason: any) => {
    console.log(reason); // "ping timeout"
  });

  return (
    <div className="App">
      {winnerName == "" ? (
        <>
          {!isGameStarted ? (
            <>
              <div className="joinStuff">
                <div className="joinCode">
                  <h2>{gameCode}</h2>
                </div>
                <JoinedList joinedPlayers={joinedPlayers} />
              </div>
              <InputSettingsDisplay gameCode={gameCode} />
            </>
          ) : (
            <>
              {[...disconnectedPlayers].map((name) => (
                <p>{name}</p>
              ))}
              <PlayerNameBox name={activePlayerName} />
              <TimeLine gameCode={gameCode} />
            </>
          )}
        </>
      ) : (
        <WinScreen name={winnerName} />
      )}
    </div>
  );
}

export default HostGame;
