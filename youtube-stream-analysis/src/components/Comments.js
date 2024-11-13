// VideoMessage.js
import React from "react";
import Avatar from "react-avatar";

function Comments({ data }) {

  const {
    author,
    comment,
    profile_image,
    sentiment,
  } = data;

  return (
    <div
      className={`${sentiment === "negative"
          ? "bg-red-200"
          : sentiment === "positive"
            ? "bg-green-200"
            : "bg-blue-200"
        }  rounded-lg p-2 shadow-md my-1 text-gray-800 text-xs`}
    >
      <div className="flex justify-between space-x-2 items-center space-y-1">
        <Avatar className="flex" src={profile_image} round size="30"/>
        <div className="flex flex-1 gap-2 flex-wrap">
        <span className="text-gray-800 font-semibold">{author}</span>
        <span className="text-gray-700 ">{comment}</span>
        </div>
      </div>
    </div>
  );
}

export default Comments;