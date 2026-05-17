import os

class Memento:
    def __init__(self, file, content):
        self.file = file
        self.content = content


class FileWriterUtility:
    def __init__(self, file):
        self.file = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        return Memento(self.file, self.content)

    def undo(self, memento):
        self.file = memento.file
        self.content = memento.content


class FileWriterCaretaker:
    """Manages an indexed history list of up to 4 mementos"""
    def __init__(self):
        self._history = []

    def save(self, writer):
        if len(self._history) >= 4:
            self._history.pop(0)  # Discard oldest state if capacity limit is reached
        self._history.append(writer.save())

    def undo(self, writer, steps=0):
        """
        steps = 0: Immediate previous state (last item in history)
        steps = 1, 2, 3: Older historical states
        """
        if not self._history:
            print("History is empty.")
            return

        # Calculating index from the back of the list
        # -1 corresponds to steps=0, -2 to steps=1, and so on.
        target_idx = -1 - steps
        try:
            target_memento = self._history[target_idx]
            writer.undo(target_memento)
            print(f"-> Undo invoked with an additional offset of ({steps}) states in the past.")
        except IndexError:
            print(f"Error: The requested undo offset level ({steps}) does not exist in the current history.")


if __name__ == '__main__':
    os.system("clear")
    print("--- POINT 5: Extended Memento History (0 to 3) ---")
    caretaker = FileWriterCaretaker()
    writer = FileWriterUtility("GFG.txt")

    # Saving successive historical configurations (State 0 to 3)
    writer.write("State 0: Initial UADER setup\n")
    caretaker.save(writer)

    writer.write("State 1: Added behavioral pattern classes\n")
    caretaker.save(writer)

    writer.write("State 2: Imported design structure frameworks\n")
    caretaker.save(writer)

    writer.write("State 3: Final compilation of Software II\n")
    caretaker.save(writer)

    # Current un-saved/disruptive state
    writer.write("Current Bad Modification: System critical crash error!\n")
    print("--- Current content before executing undo: ---")
    print(writer.content)

    # 1. Recover immediate previous state (State 3) via undo(0)
    print("\nExecuting caretaker.undo(writer, steps=0)...")
    caretaker.undo(writer, steps=0)
    print(writer.content)

    # 2. Go deeper into history (State 1) via undo(2)
    print("Executing caretaker.undo(writer, steps=2)...")
    caretaker.undo(writer, steps=2)
    print(writer.content)