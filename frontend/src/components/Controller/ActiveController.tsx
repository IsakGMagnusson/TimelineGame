import React, { useState } from "react";
import Slider from "rc-slider";
import "rc-slider/assets/index.css";

const ActiveController = (props: any) => {
  const moveCardPosition = (card_move_to: number) => {
    props.socket.emit("move_card", props.gameCode, card_move_to);
  };

  const putCard = () => {
    props.socket.emit("put_card", props.gameCode);
  };

  const [value, setValue] = useState<number>(20);

  const OnChangeEventTriggerd = (newValue: any) => {
    console.log("new Value", newValue);
    setValue(newValue);
    props.socket.emit("scroll_cards", props.gameCode, newValue);
  };

  return (
    <div className="controller-container">
      <div className="card-button-container">
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
      </div>
      <div className="card-slider-container">
        <Slider
          value={value}
          onChange={OnChangeEventTriggerd}
          step={25}
          trackStyle={{ backgroundColor: "lightblue", height: 10 }}
          railStyle={{ backgroundColor: "lightblue", height: 10 }}
          handleStyle={{
            borderColor: "lightblue",
            height: 20,
            width: 20,
            marginTop: -5,
            backgroundColor: "#00008b",
          }}
        />
      </div>
    </div>
  );
};

export default ActiveController;
