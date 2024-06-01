import React from "react";

const ActiveController = (props: any) => {
  const moveCardPosition = (card_move_to: number) => {
    props.socket.emit("move_card", props.gameCode, card_move_to);
  };

  const putCard = () => {
    props.socket.emit("put_card", props.gameCode);
    props.setControllerState(props.ControllerState.AWAITING_RESPONSE);
  };

  return (
    <>
      <button
        className="rotation-button left"
        onClick={() => {
          moveCardPosition(-1);
        }}
      >
        |------
      </button>
      <button
        className="put-card-button"
        onClick={() => {
          putCard();
        }}
      >
        Put card
      </button>
      <button
        className="rotation-button right"
        onClick={() => {
          moveCardPosition(1);
        }}
      >
        ------|
      </button>
    </>
  );
};

export default ActiveController;
