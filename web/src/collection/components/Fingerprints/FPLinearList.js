import React from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import FpLinearListItem from "./FPLinearListItem";
import FPLinearListLoadTrigger from "./FPLinearListLoadTrigger";

const useStyles = makeStyles(() => ({
  list: {
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
  },
}));

function FpLinearList(props) {
  const { children, className } = props;
  const classes = useStyles();
  return <div className={clsx(classes.list, className)}>{children}</div>;
}

FpLinearList.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]),
  className: PropTypes.string,
};

// Access item type from the container type
FpLinearList.Item = FpLinearListItem;

// Access load trigger from the container type
FpLinearList.LoadTrigger = FPLinearListLoadTrigger;

export default FpLinearList;
