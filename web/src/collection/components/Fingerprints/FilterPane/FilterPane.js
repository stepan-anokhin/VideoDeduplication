import React from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import FilterPaneHeader from "./FilterPaneHeader";

const useStyles = makeStyles((theme) => ({
  pane: {
    backgroundColor: theme.palette.background.paper,
    minWidth: 250,
  },
}));

function FilterPane(props) {
  const { onSave, onClose, className } = props;
  const classes = useStyles();
  return (
    <div className={clsx(classes.pane, className)}>
      <FilterPaneHeader onClose={onClose} onSave={onSave} />
      <div>Filters go here...</div>
    </div>
  );
}

FilterPane.propTypes = {
  onClose: PropTypes.func,
  onSave: PropTypes.func,
  className: PropTypes.string,
};

export default FilterPane;