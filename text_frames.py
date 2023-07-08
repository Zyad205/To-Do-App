import customtkinter as ctk
from settings import *
from textwrap import TextWrapper
from PIL import Image


def save_text(header, text):
    with open(f"{header}.txt", "w") as file:
        for index, item in enumerate(text):
            text[index] = item.replace("\n", "") + "\n"
        file.writelines(text)


class DoingDone(ctk.CTkScrollableFrame):

    def __init__(self, parent, column, header):
        """Create a scrollable frame"""
        # Parent init function
        super().__init__(parent, fg_color="#000000")

        # Store the main window
        self.parent = parent

        # Main font
        self.main_font = ctk.CTkFont(*TEXT_FONT)

        # Store the name of the frame to open corresponding text file
        # for saving
        self.header = header

        # To store labels
        self.labels = []
        # Save text for saving
        self.text = []

        # Will hand text warping
        self.wrap = TextWrapper()

        self.width = self.winfo_width()
        self.height = self.winfo_height()

        # Placing
        self.grid(row=1, column=column, rowspan=2, sticky="NSEW", padx=10)

    def reformat_text(self, event):
        """Reformat the labels after changing the size of the window"""
        # A builtin function
        self._parent_canvas.configure(
            scrollregion=self._parent_canvas.bbox("all"))
        
        # Only check will the frame size changed
        if event.width != self.width or event.height != self.height:
            for label_frame in self.labels:
                # Get the updated size
                self.update()
                size = label_frame.winfo_width() - 20

                # Get the original text
                label_text = label_frame.original_text
                formatted_text = self.get_formatted_text(
                    label_text, size)

                label_frame.label.configure(text=formatted_text)
            
            self.width = event.width
            self.height = event.height

    def get_formatted_text(self, text, size):
        """Return the text with \\n so the text
        won't get cropped, arguments the {text} and {size}"""
        # Check the text is not empty
        if text:
            char_size = []

            # Get the average size for every character
            for char in text:
                char_size.append(self.main_font.measure(char))

            char_size = sum(char_size) / len(char_size)

            # Get the number of characters that would fit in given size
            char_num = size / char_size

            # Update the wrap object with appropriate number
            # of characters in one line
            self.wrap.width = round(char_num)

            text_list = self.wrap.wrap(text)
            # Make the list a string again with {\\n}
            formatted_text = '\n'.join(text_list)
        else:
            formatted_text = ""
        return formatted_text

    def add_label(self, label_text):
        """Takes a the label text and add a label to the frame"""

        # Get the index for the new label
        index = len(self.labels)

        # Create a new label
        label_frame = Label(
            self,
            self.get_out_of_frame,
            self.main_font,
            index,
            self.delete_label)

        # Save the new label
        self.labels.append(label_frame)

        # Packing it
        label_frame.pack(fill="x", pady=5)

        # Getting updated sized of the label
        self.update()
        size = label_frame.label.winfo_width() - 20

        # Getting the text with the {\n} 
        formatted_text = self.get_formatted_text(label_text, size)

        # Give the label the original text
        label_frame.original_text = label_text

        # Puts the formatted text on the label
        label_frame.label.configure(text=formatted_text)

        # Save the text of the label for saving it
        self.text.append(label_text)
        save_text(self.header, self.text)

    def delete_label(self, index):
        """Takes the index of the label and delete it"""

        # Destroy the label
        current_label = self.labels[index]
        current_label.destroy()

        # Deleting the text and labels
        del self.text[index]
        del self.labels[index]
        
        # Reindex all the labels
        for index, label in enumerate(self.labels):
            label.index = index

        # Resave the text
        save_text(self.header, self.text)

    def get_out_of_frame(self, index):
        """When a the label is hold on it's get destroyed then create a new
        one out of the text frames then follow the mouse"""

        # Get the current label
        current_label = self.labels[index]
        # Getting current text and the original text without formatting
        text = current_label.label.cget("text")
        original_text = current_label.original_text

        # Get the width of the label
        width = current_label.winfo_width()

        # Destroy current label
        current_label.destroy()

        # Delete the label from our list
        del self.labels[index]

        # Create a new label out of any text frames
        new_label = Label(self.parent, None, self.main_font, index, self.delete_label,
                          out_out_frame=True, parents_list=self.parents_list)
        # Give the label the original text without {\n}
        new_label.original_text = original_text

        # Configuration
        new_label.label.configure(text=text, width=width)

        # Put the center of the label on the mouse position
        root = new_label.winfo_toplevel()
        x, y = root.winfo_pointerxy()
        new_label.place(
            x=x - root.winfo_rootx(),
            y=y - root.winfo_rooty(),
            anchor="center")

        # Reindex the labels
        for index, label_frame in enumerate(self.labels):
            label_frame.index = index
        
        # Deleting the text of the label from out list then save the changes 
        del self.text[index]
        save_text(self.header, self.text)


class ToDo(ctk.CTkScrollableFrame):

    def __init__(self, parent, header):
        """Create a scrollable frame"""

        # Parent init function
        super().__init__(parent, fg_color="#000000")
        # Main font
        self.main_font = ctk.CTkFont(*TEXT_FONT)

        # Store the name of the frame to open corresponding text file
        # for saving
        self.header = header

        # Make a input frame
        self.text_input = TextInput(
            self,
            self.add_label,
            self.close_input,
            self.main_font)
        # Self Layout
        self.grid(row=1, column=0, rowspan=2, sticky="NSEW", padx=10)
        self.wrap = TextWrapper()

        self.parent = parent
        self.labels = []
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.text = []

        self.bind("<Configure>", self.reformat_text)

    def add_label(self, label_text):
        if not label_text or label_text.isspace():
            pass
        else:
            index = len(self.labels)
            label_frame = Label(self, self.get_out_of_frame,
                                self.main_font, index, self.delete_label)
            label_frame.original_text = label_text

            self.text.append(label_text)

            save_text(self.header, self.text)

            self.labels.append(label_frame)

            label_frame.pack(fill="x", pady=5)
            self.update()
            size = label_frame.winfo_width() - 20

            formatted_text = self.get_formatted_text(text=label_text, size=size)

            label_frame.label.configure(text=formatted_text)
            if self.text_input.winfo_ismapped():
                self.text_input.pack_forget()
                self.text_input.pack(fill="x", padx=1, pady=1)

    def close_input(self):
        self.grid_forget()
        self.grid(row=1, column=0, rowspan=2, sticky="NSEW")
        self.create_input_frame = CreateInputFrame(
            self.parent, self.open_input, self.main_font)
        self.text_input.pack_forget()

    def open_input(self):
        self.grid_forget()
        self.grid(row=0, column=0, rowspan=2, sticky="NSEW", padx=10)
        self.create_input_frame.grid_forget()
        self.text_input.pack(fill="x")

    def reformat_text(self, event):
        self._parent_canvas.configure(
            scrollregion=self._parent_canvas.bbox("all"))
        if event.width != self.width or event.height != self.height:
            for label_frame in self.labels:

                self.update()
                size = label_frame.winfo_width() - 20
                label_text = label_frame.original_text
                formatted_text = self.get_formatted_text(
                    text=label_text, size=size)

                label_frame.label.configure(text=formatted_text)
            self.width = event.width
            self.height = event.height

    def delete_label(self, index):
        current_label = self.labels[index]
        current_label.destroy()

        del self.text[index]
        del self.labels[index]

        save_text(self.header, self.text)

        for index, label in enumerate(self.labels):
            label.index = index

    def get_out_of_frame(self, index):

        current_label = self.labels[index]
        text = current_label.label.cget("text")
        original_text = current_label.original_text
        width = current_label.winfo_width()
        current_label.destroy()

        del self.text[index]
        del self.labels[index]
        
        save_text(self.header, self.text)

        new_label = Label(self.parent, None, self.main_font, index, self.delete_label, out_out_frame=True,
                          parents_list=self.parents_list)
        new_label.original_text = original_text
        new_label.label.configure(text=text, cursor="fleur", width=width)

        root = new_label.winfo_toplevel()

        x, y = root.winfo_pointerxy()

        new_label.place(
            x=x - root.winfo_rootx(),
            y=y - root.winfo_rooty(),
            anchor="center")

    def get_formatted_text(self, text, size):
        if text:
            char_size = []
            for char in text:
                char_size.append(self.main_font.measure(char))

            char_size = sum(char_size) / len(char_size)
            char_num = size / char_size
            self.wrap.width = round(char_num)

            text_list = self.wrap.wrap(text)
            formatted_text = '\n'.join(text_list)
        else:
            formatted_text = ""
        return formatted_text


class Label(ctk.CTkFrame):

    def __init__(self, parent, move_func, font, index, delete_func, out_out_frame=False, parents_list=None):
        super().__init__(parent, corner_radius=2, fg_color="transparent")

        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")

        self.close_image = Image.open("delete.png")

        self.close_image_tk = ctk.CTkImage(self.close_image)

        self.label = ctk.CTkLabel(
            self,
            justify="left",
            font=font,
            fg_color=INPUT_TEXT_COLOR,
            corner_radius=5,
            anchor="w")
        self.label.grid(row=0, column=0, sticky="NSEW")

        self.delete_button = ctk.CTkButton(
            self,
            text="",
            command=lambda: self.delete_func(),
            fg_color=TEXT_FRAMES_COLOR,
            bg_color=TEXT_FRAMES_COLOR,
            hover_color="#FF0000",
            image=self.close_image_tk)

        self.index = index
        self.parents_list = parents_list
        self.first_time = True
        self.close_func = delete_func
        self.can_unshow = True

        if not out_out_frame:
            self.label.bind("<B1-Motion>", lambda _: move_func(self.index))
            self.label.bind("<Leave>", self.unshow_delete)
            self.label.bind("<Enter>", self.show_delete)

        else:
            self.bind("<B1-Motion>", self.move)
            self.released = False
            self.label.bind("<ButtonRelease-1>", self.small_func)
            self.move(0)

    def move(self, _):
        root = self.winfo_toplevel()
        self.place(
            x=root.winfo_pointerx() - root.winfo_rootx(),
            y=root.winfo_pointery() - root.winfo_rooty(),
            anchor="center")
        if self.first_time:
            self.label.unbind("<B1-Motion>")
            self.first_time = False
        if not self.released:
            self.last_func = self.after(10, lambda: self.move(0))
        else:
            self.after_cancel(self.last_func)
            self.release()

    def release(self):

        root = self.winfo_toplevel()

        x_pos = root.winfo_pointerx() - root.winfo_rootx()
        one_column = round(root.winfo_width() / 3)
        first_point = one_column / 2
        second_point = first_point + one_column
        third_point = second_point + one_column

        first_point = abs(first_point - x_pos)
        second_point = abs(second_point - x_pos)
        third_point = abs(third_point - x_pos)

        temp_dict = {first_point: self.parents_list[0],
                     second_point: self.parents_list[1],
                     third_point: self.parents_list[2]}

        parent = temp_dict[min(first_point, second_point, third_point)]
        self.released = True
        text = self.original_text
        parent.add_label(text)
        self.destroy()

    def small_func(self, _):
        self.released = True

    def delete_func(self):
        self.close_func(self.index)

    def show_delete(self, _):
        self.delete_button.place(
            relx=0.9, rely=0.5, anchor="center", relheight=0.7, relwidth=0.1)

    def unshow_delete(self, event):
        if event.y < 0 or event.y > self.winfo_height() or event.x < 0 or event.x > self.winfo_width():
            self.delete_button.place_forget()


class TextInput(ctk.CTkFrame):
    def __init__(self, parent, add_label_func, close_input, font):
        super().__init__(parent, fg_color="transparent")

        # Layout
        self.columnconfigure(tuple(range(5)), weight=1, uniform="a")
        self.rowconfigure(0, weight=2, uniform="b")
        self.rowconfigure(1, weight=1, uniform="b")

        # Input Entry
        self.input = ctk.CTkTextbox(
            self,
            height=65,
            fg_color=INPUT_TEXT_COLOR,
            font=font)

        self.add_label_func = add_label_func

        self.add_button = ctk.CTkButton(
            self,
            text="Add card",
            fg_color=ADD_BUTTON["color"]["bg"],
            hover_color=ADD_BUTTON["color"]["hover"],
            text_color=ADD_BUTTON["color"]["text"],
            width=1,
            command=self.add_label)

        self.input.grid(row=0, column=0, columnspan=5, sticky="NSEW")
        self.input.bind("<Shift-Return>", lambda _: self.add_label())
        self.add_button.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="NSEW",
            pady=7)

        self.close_button = ctk.CTkButton(
            self,
            text="X",
            fg_color="transparent",
            hover_color="#FF0000",
            command=close_input)

        self.close_button.grid(row=1, column=2, sticky="NSEW", pady=7, padx=7)

        self.pack(fill="x")

    def add_label(self):
        text = self.input.get(1.0, "end")
        self.add_label_func(text)
        self.input.delete(1.0, "end")


class CreateInputFrame(ctk.CTkFrame):

    def __init__(self, parent, open_func, font):
        super().__init__(parent, fg_color="transparent")

        self.label = ctk.CTkButton(
            self, text="+ Add a card", font=font, height=1, width=1, command=open_func,
            fg_color="#000000", hover_color="#282f28")

        self.label.pack(fill="x", pady=2)

        self.grid(row=2, column=0, sticky="NSEW")
