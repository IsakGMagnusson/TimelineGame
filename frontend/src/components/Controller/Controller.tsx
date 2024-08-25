import React, { useEffect, useState } from "react";
import ActiveController from "./ActiveController";
import AwaitingResponseController from "./AwaitingResponseController";
import TurnDecisionController from "./TurnDecisionController";
import { Controller_State } from "../../interfaces";

const Controller = (props: any) => {
  const [controllerState, setControllerState] = useState<Controller_State>(
    Controller_State.ACTIVE
  );

  useEffect(() => {
    console.log("aaa");
    props.socket.emit("fetch_controller_state", props.gameCode);
  }, []);

  useEffect(() => {
    props.socket.on("set_controller_state", function (data: any) {
      console.log(data.controller_state);
      setControllerState(data.controller_state);
    });
  }, []);

  function loadControllerFromState(state: Controller_State) {
    if (state == Controller_State.ACTIVE)
      return (
        <ActiveController
          socket={props.socket}
          gameCode={props.gameCode}
          ControllerState={Controller_State}
        />
      );
    else if (state == Controller_State.AWAITING_RESPONSE)
      return <AwaitingResponseController />;
    else if (state == Controller_State.TURN_DECISION)
      return (
        <TurnDecisionController
          socket={props.socket}
          gameCode={props.gameCode}
        />
      );
    else if (state == Controller_State.INACTIVE)
      return <div>Not your turn!</div>;
  }

  return <>{loadControllerFromState(controllerState)}</>;
};

export default Controller;
