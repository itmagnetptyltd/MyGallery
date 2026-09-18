"""Criteria 2, 3 and 4 — what the written start instructions promise.

Criterion 2 ("followed by someone who has not worked on the project") is a
human check. These tests cover what can be checked mechanically; the e2e boot
test is the closest proxy for the rest.
"""

# @covers REQ-GAL-011@v1
def test_the_start_instructions_name_exactly_one_prerequisite(prerequisites):
    assert len(prerequisites) == 1


# @covers REQ-GAL-011@v1
def test_the_named_prerequisite_is_python(prerequisites):
    assert "python" in prerequisites[0].lower()


# @covers REQ-GAL-011@v1
def test_the_start_instructions_reach_a_running_application_in_a_single_step(run_steps):
    assert len(run_steps) == 1


# @covers REQ-GAL-011@v1
def test_the_documented_start_file_exists(project_root, documented_start_file):
    assert (project_root / documented_start_file).is_file()
