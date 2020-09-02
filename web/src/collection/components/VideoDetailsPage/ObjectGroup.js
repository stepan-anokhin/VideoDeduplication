import React from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import ObjectType from "./ObjectType";
import usePopup from "../../../common/hooks/usePopup";
import ObjectGroupPopper from "./ObjectGroupPopper";

const useStyles = makeStyles((theme) => ({
  objectGroup: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: theme.palette.primary.main,
    cursor: "pointer",
    position: "absolute",
    top: "50%",
  },
}));

/**
 * Get relative start position of the group
 */
function relativePosition(objects, fullLength) {
  const first = Math.min(...objects.map((object) => object.position));
  return first / fullLength;
}

/**
 * Convert fraction to CSS Percents
 */
function percents(value) {
  return `${(value * 100).toFixed(2)}%`;
}

/**
 * A point on the video timeline representing a close group
 * of recognized objects.
 */
function ObjectGroup(props) {
  const { objects, fullLength, onJump, className } = props;
  const classes = useStyles();
  const { popup, clickTrigger } = usePopup("object-group");

  const left = percents(relativePosition(objects, fullLength));

  return (
    <React.Fragment>
      <div
        className={clsx(classes.objectGroup, className)}
        style={{ left }}
        {...clickTrigger}
      />
      <ObjectGroupPopper objects={objects} onJump={onJump} {...popup} />
    </React.Fragment>
  );
}

ObjectGroup.propTypes = {
  /**
   * Full video-file length in milliseconds
   */
  fullLength: PropTypes.number.isRequired,
  /**
   * Objects comprising the group.
   */
  objects: PropTypes.arrayOf(ObjectType).isRequired,
  /**
   * Handle jump to a particular object
   */
  onJump: PropTypes.func,
  className: PropTypes.string,
};

export default ObjectGroup;