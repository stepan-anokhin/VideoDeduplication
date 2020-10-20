import itertools
from dataclasses import dataclass, field
from typing import List

from sqlalchemy import Column
from sqlalchemy.orm import joinedload

from db.schema import Files, Matches


def _chunks(iterable, size=100):
    """Split iterable into equal-sized chunks."""
    iterator = iter(iterable)
    chunk = list(itertools.islice(iterator, size))
    while chunk:
        yield chunk
        chunk = list(itertools.islice(iterator, size))


@dataclass
class FileMatchesRequest:
    """List single file's matches request."""
    file: Files
    limit: int = 20
    offset: int = 0
    max_distance: float = 1.0
    min_distance: float = 0.0
    hops: int = 1
    preload: List[Column] = field(default_factory=list)


@dataclass
class FileMatchesResult:
    """List single file's matches results."""
    files: List[Files]
    matches: List[Matches]


class MatchesDAO:
    """Data-access object for file matches."""

    @staticmethod
    def list_file_matches(req: FileMatchesRequest, session) -> FileMatchesResult:
        """List single file's matches."""
        files = []
        matches = []
        seen_matches = set()
        # ids of files that was loaded during previous
        # steps or will be loaded during the current step
        seen = {req.file.id}
        # ids of files that will be loaded during the current step
        current_step = {req.file.id}
        # 'step' variable is always equal to the minimal distance (number of arrows)
        # from the source file to the files that will be loaded during the current step
        for step in range(req.hops + 1):
            # ids of files that will be loaded during the next step
            next_step = set()
            more_steps = step < req.hops

            # Perform current step in equal-sized chunks
            for chunk in _chunks(current_step):
                query = session.query(Files).options(
                    joinedload(Files.source_matches),
                    joinedload(Files.target_matches))
                query = MatchesDAO._preload_file_attrs(query, req.preload)
                items = query.filter(Files.id.in_(chunk)).all()
                for file in items:
                    files.append(file)
                    if more_steps:
                        MatchesDAO._populate_next_step(file, seen, next_step)
            seen.update(next_step)
            current_step = next_step
        matches = MatchesDAO._extract_matches(files, file_ids=seen)
        return FileMatchesResult(files=files, matches=matches)

    @staticmethod
    def _populate_next_step(file, seen, next_step):
        """Add not-seen files to the next step."""
        for match in file.source_matches:
            matched_file = match.match_video_file
            if matched_file.id not in seen:
                next_step.add(matched_file.id)
        for match in file.target_matches:
            matched_file = match.query_video_file
            if matched_file.id not in seen:
                next_step.add(matched_file.id)

    @staticmethod
    def _preload_file_attrs(query, preload):
        """Preload requested optional file attributes."""
        for relation in preload:
            query = query.options(joinedload(relation))
        return query

    @staticmethod
    def _extract_matches(files, file_ids):
        """Build matches list."""
        matches = []
        for file in files:
            for match in file.target_matches:
                if match.match_video_file_id in file_ids and match.query_video_file_id in file_ids:
                    matches.append(match)
            for match in file.source_matches:
                if match.match_video_file_id in file_ids and match.query_video_file_id in file_ids:
                    matches.append(match)
        return matches

    @staticmethod
    def _apply_match_filters(query, req):
        """Apply filters by match attributes."""
