import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { DeadlineList } from "./DeadlineList";

function addDeadline(title: string, dueDate: string) {
  fireEvent.change(screen.getByLabelText("Title"), {
    target: { value: title },
  });
  fireEvent.change(screen.getByLabelText("Due Date"), {
    target: { value: dueDate },
  });
  fireEvent.submit(screen.getByTestId("deadline-form"));
}

describe("DeadlineList", () => {
  it("renders the form and empty state", () => {
    render(<DeadlineList />);
    expect(screen.getByText("Add New Deadline")).toBeInTheDocument();
    expect(screen.getByText("No deadlines yet. Add one above to get started.")).toBeInTheDocument();
  });

  it("adds a new deadline", () => {
    render(<DeadlineList />);
    addDeadline("Test Deadline", "2026-12-31");
    expect(screen.getByText("Test Deadline")).toBeInTheDocument();
  });

  it("toggles a deadline as complete", () => {
    render(<DeadlineList />);
    addDeadline("Complete me", "2026-12-31");
    fireEvent.click(screen.getByLabelText("Mark complete"));
    expect(screen.getByText("Completed")).toBeInTheDocument();
  });

  it("deletes a deadline", () => {
    render(<DeadlineList />);
    addDeadline("Delete me", "2026-12-31");
    expect(screen.getByText("Delete me")).toBeInTheDocument();
    fireEvent.click(screen.getByLabelText("Delete deadline"));
    expect(screen.queryByText("Delete me")).not.toBeInTheDocument();
  });
});
