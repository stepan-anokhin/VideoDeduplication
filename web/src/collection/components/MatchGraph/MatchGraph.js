import React, { useEffect, useRef } from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import D3Graph from "./D3Graph";
import MatchType from "../FileMatchesPage/MatchType";
import FileType from "../FileBrowserPage/FileType";

const useStyles = makeStyles(() => ({
  root: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  content: {
    height: 500,
  },
}));

/**
 * Get collection of links compatible with D3Graph.
 */
function getLinks(source, matches) {
  return matches.map((match) => ({
    source: match.source,
    target: match.target,
    value: 10 * (1 - match.distance),
  }));
}

/**
 * Get collection of nodes compatible with D3Graph
 */
function getNodes(source, files) {
  return [
    ...Object.values(files).map((file) => ({
      id: file.id,
      group: file.id === source.id ? 2 : 1,
    })),
  ];
}

function MatchGraph(props) {
  const { source, matches, files, className } = props;
  const classes = useStyles();
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current != null) {
      const graph = new D3Graph({
        links: getLinks(source, matches),
        nodes: getNodes(source, files),
        container: ref.current,
        classes: { content: classes.content },
      });
      graph.display();
    }
  }, [ref.current, source, matches]);

  return (
    <div className={clsx(classes.root, className)}>
      <svg ref={ref} />
    </div>
  );
}

MatchGraph.propTypes = {
  /**
   * A initial file for which all similar files were selected
   */
  source: FileType.isRequired,
  /**
   * Similarity relationship between files
   */
  matches: PropTypes.arrayOf(MatchType).isRequired,
  /**
   * Similar files map
   */
  files: PropTypes.object.isRequired,
  className: PropTypes.string,
};

export default MatchGraph;
