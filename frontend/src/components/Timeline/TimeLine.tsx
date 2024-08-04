import React, { useEffect, useRef, useState } from "react";
import { CardData, Card_State } from "../../interfaces";
import Card from "./Card";
import { socket } from "../../Socket";
import * as Utils from "../../util/Utils";

const TimeLine = (props: any) => {
  const [activeCardDisplayDate, setActiveCardDisplayDate] =
    useState<string>("????");
  const [allActiveCards, setAllActiveCards] = useState<CardData[]>([]);

  function timeout(delay: number) {
    return new Promise((res) => setTimeout(res, delay));
  }

  const elementRef = useRef<HTMLDivElement>(null);

  const [scrollTop, setScrollTop] = useState(0);
  async function revealDate(date: number) {
    const dateString = date.toString();

    for (let i = 0; i <= dateString.length; i++) {
      setActiveCardDisplayDate(dateString.substring(0, i).padEnd(4, "?"));
      await timeout(300);
    }
  }

  useEffect(() => {
    function fetch_cards(data: any) {
      setAllActiveCards(data.all_cards);
    }

    async function on_put_card_incorrect(data: any) {
      await revealDate(data.active_card.date);
      setAllActiveCards(data.sorted_cards);
      await timeout(3000); // run animation (based on state)
      setAllActiveCards([]);
      socket.emit("go_next_turn", props.gameCode);
    }

    function move_card(data: any) {
      setAllActiveCards(
        Utils.swapItemsInArray(data.old_index, data.new_index, [
          ...allActiveCards,
        ])
      );
    }

    function draw_card(data: any) {
      setAllActiveCards(data.all_cards);
    }

    async function put_card_correct(data: any) {
      await revealDate(data.active_card.date);
      setAllActiveCards(data.all_cards);
      setActiveCardDisplayDate("????");
      socket.emit("draw_card_or_new_turn", props.gameCode);
      props.setScore(data.all_cards.length);
    }

    function new_turn(data: any) {
      setAllActiveCards(data.all_cards);
      setActiveCardDisplayDate("????");
      props.setScore(data.all_cards.length - 1);
    }

    function scroll_cards(data: any) {
      const windowWidth = window.innerWidth;
      const elementTotalWidth = elementRef.current!.scrollWidth;
      const convertedScrollPercent = (elementTotalWidth - windowWidth) / 100;

      elementRef.current!.scrollLeft =
        data.scroll_percent * convertedScrollPercent;
    }

    socket.on("put_card_incorrect", on_put_card_incorrect);
    socket.on("move_card", move_card);
    socket.on("draw_card", draw_card);
    socket.on("put_card_correct", put_card_correct);
    socket.on("new_turn", new_turn);
    socket.on("fetch_cards", fetch_cards);
    socket.on("scroll_cards", scroll_cards);

    return () => {
      socket.off("put_card_incorrect", on_put_card_incorrect);
      socket.off("move_card", move_card);
      socket.off("draw_card", draw_card);
      socket.off("put_card_correct", put_card_correct);
      socket.off("new_turn", new_turn);
      socket.off("fetch_cards", fetch_cards);
      socket.off("scroll_cards", scroll_cards);
    };
  }, [allActiveCards]);

  useEffect(() => {
    socket.emit("fetch_cards", props.gameCode);
  }, []);

  return (
    <div className="card-holder" ref={elementRef}>
      <div className="active-cards">
        {[...allActiveCards]
          .filter((card) => card.state != Card_State.REMOVED)
          .map((card: CardData) => (
            <div>
              <Card card={card} activeCardDisplayDate={activeCardDisplayDate} />
            </div>
          ))}
      </div>
    </div>
  );
};

export default TimeLine;
