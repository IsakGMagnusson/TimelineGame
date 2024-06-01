import React, { useEffect, useState } from "react";
import ActiveController from "./ActiveController";
import AwaitingResponseController from "./AwaitingResponseController";
import TurnDecisionController from "./TurnDecisionController";

const Controller = (props: any) => {
  enum ControllerState {
    ACTIVE = "active",
    TURN_DECISION = "turn_decision",
    AWAITING_RESPONSE = "awaiting_response",
  }

  const [controllerState, setControllerState] = useState<ControllerState>(
    ControllerState.ACTIVE
  );

  useEffect(() => {
    props.socket.on("put_card_correct", function () {
      setControllerState(ControllerState.TURN_DECISION);
    });
  }, []);

  useEffect(() => {
    props.socket.on("new_turn", function () {
      setControllerState(ControllerState.ACTIVE);
    });
  }, []);

  function loadControllerFromState(state: ControllerState) {
    if (state == ControllerState.ACTIVE)
      return (
        <ActiveController
          socket={props.socket}
          gameCode={props.gameCode}
          setControllerState={setControllerState}
          ControllerState={ControllerState}
        />
      );
    else if (state == ControllerState.AWAITING_RESPONSE)
      return <AwaitingResponseController />;
    else if (state == ControllerState.TURN_DECISION)
      return (
        <TurnDecisionController
          socket={props.socket}
          gameCode={props.gameCode}
          setControllerState={setControllerState}
          ControllerState={ControllerState}
        />
      );
  }

  return <>{loadControllerFromState(controllerState)}</>;
};

export default Controller;
