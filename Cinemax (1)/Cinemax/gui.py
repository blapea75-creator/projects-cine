import tkinter as tk
from tkinter import messagebox, simpledialog
from calculate import calculate_total, calculate_change
from points import redeem_discount, earn_points
from tkinter import ttk
from transaction import save_transaction, get_transaction_count, get_all_transactions

# Movies and available ticket stock
movies = {
    "Avengers": {"Regular": 30, "VIP": 20},
    "Spiderman": {"Regular": 30, "VIP": 20},
    "Minecraft": {"Regular": 30, "VIP": 20}
}
# Store occupied seats separately for each movie
occupied_seats = {movie_name: set() for movie_name in movies}

users = {}
sales = 0
user = None
root = None
transaction_counter = 0

# Start the program
def start_gui():
    global root
    root = tk.Tk()
    root.title("Cine-Max")
    root.geometry("400x500")
    welcome()
    root.mainloop()

# Clear the current screen
def clear():
    for item in root.winfo_children():
        item.destroy()

# Create a button
def button(text, command):
    tk.Button(root,text=text,command=command,width=25).pack(pady=5)

# Generate an incrementing transaction ID
def generate_transaction_id():
    global transaction_counter

    transaction_counter += 1
    return f"TXN-{transaction_counter:04d}"

# Welcome screen
def welcome():
    clear()
    tk.Label(root,text="CINE-MAX",font=("Arial", 22, "bold")).pack(pady=20)
    button("Login", login)
    button("Register Membership", register)
    button("Continue as Guest", guest)
    tk.Label(root,pady=100).pack()
    button("Help", shelp)

# Login screen
def login():
    clear()
    tk.Label(root, text="Username").pack()
    name = tk.Entry(root)
    name.pack()

    tk.Label(root, text="Password").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    def check_login():
        global user
        username = name.get().strip()
        user_password = password.get()

        if username == "admin" and user_password == "admin":
            user = None
            admin()

        elif (
            username in users
            and users[username]["password"] == user_password
        ):
            user = username
            booking()

        else:
            messagebox.showerror("Error","Wrong username or password")

    button("Login", check_login)
    button("Back", welcome)

# Register membership
def register():
    clear()
    tk.Label(root, text="Create Username (minimum 4 characters)").pack()
    name = tk.Entry(root)
    name.pack()

    tk.Label(root, text="Create Password (minimum 8 characters)").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    def save_member():
        username = name.get().strip()
        user_password = password.get()

        if username == "" or user_password == "":
            messagebox.showerror("Error","Please fill in all fields.")

        elif len(username) < 4:
            messagebox.showerror("Invalid Username","Username must be at least 4 characters long.")

        elif len(user_password) < 8:
            messagebox.showerror("Invalid Password","Password must be at least 8 characters long.")

        elif username.lower() == "admin" or username in users:
            messagebox.showerror("Error","Username already exists or is reserved.")

        else:
            users[username] = {"password": user_password,"points": 0}
            messagebox.showinfo("Success","Membership created successfully!")
            login()

    button("Register", save_member)
    button("Back", welcome)

# Continue as a guest
def guest():
    global user
    user = None
    booking()

# Help button
def shelp():
    messagebox.showinfo("Help","Contact in Person: Ron Francis Serrano\n""Phone Number: 09123456789\n""Email Address: ronfrancis@gmail.com")

# Booking screen
def booking():
    clear()

    tk.Label(root,text="CINE-MAX BOOKING",font=("Arial", 18, "bold")).pack(pady=10)

    # Movie selection
    tk.Label(root, text="Choose Movie").pack()
    movie = tk.StringVar(value="Choose Movie")
    tk.OptionMenu(root,movie,*movies.keys()).pack()

    # Ticket type
    tk.Label(root, text="Ticket Type").pack()
    ticket = tk.StringVar(value="Choose Ticket")
    tk.OptionMenu(root,ticket,"Regular","VIP").pack()
    tk.Label(root,text="Regular: ₱250 | VIP: ₱400").pack(pady=3)

    # Quantity
    tk.Label(root, text="Quantity").pack()
    quantity = tk.Entry(root)
    quantity.insert(0, "1")
    quantity.pack()

    # Seat selection

    # Seat selection
    tk.Label(root, text="Choose Seat").pack(pady=5)

    seat_frame = tk.Frame(root)
    seat_frame.pack()

    row_choice = tk.StringVar(value="A")
    column_choice = tk.StringVar(value="1")

    tk.Label(seat_frame, text="Row").pack(side="left")

    tk.OptionMenu(
        seat_frame,
        row_choice,
        *["A", "B", "C", "D", "E"]
    ).pack(side="left")

    tk.Label(seat_frame, text="Column").pack(side="left")

    tk.OptionMenu(
        seat_frame,
        column_choice,
        *[str(i) for i in range(1, 11)]
    ).pack(side="left")

    selected_seats = []

    seat_label = tk.Label(
        root,
        text="Selected Seats: None",
        wraplength=350
    )
    seat_label.pack(pady=3)



    def add_seat():
        movie_name = movie.get()
        ticket_type = ticket.get()

        if movie_name not in movies:
            messagebox.showerror("Error", "Choose a movie first")
            return

        if ticket_type not in ("Regular", "VIP"):
            messagebox.showerror("Error", "Choose a ticket type first")
            return

        row = row_choice.get()
        seat_name = row + column_choice.get()

        # Regular seats are rows A-C
        if ticket_type == "Regular" and row not in ["A", "B", "C"]:
            messagebox.showerror(
                "Invalid Seat",
                "Regular seats are only in rows A, B, and C."
            )
            return

        # VIP seats are rows D-E
        if ticket_type == "VIP" and row not in ["D", "E"]:
            messagebox.showerror(
                "Invalid Seat",
                "VIP seats are only in rows D and E."
            )
            return

        if seat_name in occupied_seats[movie_name]:
            messagebox.showerror(
                "Error",
                seat_name + " is already occupied"
            )
            return

        if seat_name in selected_seats:
            messagebox.showerror("Error", "Seat already selected")
            return

        selected_seats.append(seat_name)
        seat_label.config(
            text="Selected Seats: " + ", ".join(selected_seats)
        )

    button("Add Seat", add_seat)


    # Payment
    tk.Label(root, text="Payment").pack()

    payment = tk.Entry(root)
    payment.pack()

    # Member loyalty points
    if user:
        tk.Label(root,text="Loyalty Points: "+ str(users[user]["points"])).pack(pady=5)

    # Purchase tickets
    def buy():
        global sales

        try:
            qty = int(quantity.get())
            paid = float(payment.get())

            if qty <= 0 or paid < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror("Error","Enter a valid quantity and payment")
            return

        movie_name = movie.get()
        ticket_type = ticket.get()

        if movie_name not in movies:
            messagebox.showerror("Error","Choose a movie")
            return

        if ticket_type not in ("Regular", "VIP"):
            messagebox.showerror("Error","Choose a ticket type")
            return

        # One seat is required for each ticket
        if len(selected_seats) != qty:
            messagebox.showerror("Error","Select exactly one seat for each ticket")
            return

        # Check that selected seats are still available
        for seat_name in selected_seats:
            if seat_name in occupied_seats[movie_name]:
                messagebox.showerror("Error",seat_name + " is already occupied")
                return

        available = movies[movie_name][ticket_type]

        if qty > available:
            messagebox.showerror("Error","Not enough tickets available")
            return

        # Calculate ticket price
        if ticket_type == "Regular":
            price = 250
        else:
            price = 400

        total = calculate_total(price, qty)
        points_used = 0

        # Member discount
        if user and users[user]["points"] >= 100:
            answer = messagebox.askyesno("Rewards","Use 100 points for a ₱50 discount?")

            if answer:
                total, remaining_points = redeem_discount(users[user]["points"],total)

                users[user]["points"] = remaining_points
                points_used = 100

        # Check payment before completing purchase
        if paid < total:
            messagebox.showerror(
                "Error",
                f"Insufficient payment!\nTotal: ₱{total:.2f}"
            )

            if user and points_used > 0:
                users[user]["points"] += points_used

            return

        # Complete successful purchase
        change = calculate_change(paid, total)

        transaction_id = save_transaction(
            movie=movie_name,
            ticket_type=ticket_type,
            quantity=qty,
            seats=selected_seats,
            total=total,
            payment=paid,
            change_amount=change,
            username=user if user else "Guest"
        )

        change = calculate_change(paid, total)

        for seat_name in selected_seats:
            occupied_seats[movie_name].add(seat_name)

        movies[movie_name][ticket_type] -= qty
        sales += total

        if user:
            users[user]["points"] += earn_points(total)
            points = users[user]["points"]
        else:
            points = "Guest"

        remaining = movies[movie_name][ticket_type]

        # Receipt
        messagebox.showinfo(
            "Receipt",
            f"Transaction ID: {transaction_id}\n"
            f"Movie: {movie_name}\n"
            f"Ticket: {ticket_type}\n"
            f"Quantity: {qty}\n"
            f"Seats: {', '.join(selected_seats)}\n"
            f"Total: ₱{total:.2f}\n"
            f"Payment: ₱{paid:.2f}\n"
            f"Change: ₱{change:.2f}\n"
            f"Remaining Tickets: {remaining}\n"
            f"Loyalty Points: {points}"
        )

        booking()

    button("Buy Ticket", buy)
    button("Redeem Free Ticket", free_ticket)
    button("Back / Logout", welcome)


# Redeem 250 points for one free Regular ticket
def free_ticket():
    global transaction_counter

    if not user:
        messagebox.showerror(
            "Error",
            "Only members can redeem free tickets"
        )
        return

    movie_name = simpledialog.askstring(
        "Choose Movie",
        "Enter the movie name:\n"
        + ", ".join(movies.keys())
    )

    if movie_name is None:
        return

    movie_name = movie_name.strip()

    if movie_name not in movies:
        messagebox.showerror(
            "Error",
            "Invalid movie"
        )
        return

    if users[user]["points"] < 250:
        messagebox.showerror(
            "Error",
            "You need 250 points"
        )
        return

    if movies[movie_name]["Regular"] <= 0:
        messagebox.showerror(
            "Error",
            "No Regular tickets available"
        )
        return

    row = simpledialog.askstring(
        "Choose Row",
        "Enter row A-Z:"
    )

    if row is None:
        return

    row = row.strip().upper()

    if row not in ["A", "B", "C"]:
        messagebox.showerror(
            "Error",
            "Invalid row"
        )
        return

    column = simpledialog.askinteger(
        "Choose Column",
        "Enter column 1-10:",
        minvalue=1,
        maxvalue=10
    )

    if column is None:
        return

    seat_name = row + str(column)

    if seat_name in occupied_seats[movie_name]:
        messagebox.showerror(
            "Error",
            "This seat is already occupied"
        )
        return

    answer = messagebox.askyesno(
        "Confirm",
        f"Redeem 250 points for one free ticket?\n"
        f"Movie: {movie_name}\n"
        f"Seat: {seat_name}"
    )

    if answer:
        transaction_id = save_transaction(
            movie=movie_name,
            ticket_type="Regular (Free)",
            quantity=1,
            seats=[seat_name],
            total=0,
            payment=0,
            change_amount=0,
            username=user
        )

        users[user]["points"] -= 250
        movies[movie_name]["Regular"] -= 1
        occupied_seats[movie_name].add(seat_name)

        messagebox.showinfo(
            "Receipt",
            f"Transaction ID: {transaction_id}\n"
            f"Movie: {movie_name}\n"
            f"Ticket: Regular (Free)\n"
            f"Seat: {seat_name}\n"
            f"Points Used: 250\n"
            f"Remaining Points: {users[user]['points']}"
        )

        booking()


# Add ticket stock
def add_ticket_quantity():
    movie_name = simpledialog.askstring(
        "Movie",
        "Enter movie name:\n" + ", ".join(movies.keys())
    )

    if movie_name is None:
        return

    movie_name = movie_name.strip()

    if movie_name not in movies:
        messagebox.showerror(
            "Error",
            "Invalid movie"
        )
        return

    ticket_type = simpledialog.askstring(
        "Ticket Type",
        "Enter Regular or VIP:"
    )

    if ticket_type is None:
        return

    ticket_type = ticket_type.strip().lower()

    if ticket_type == "regular":
        ticket_type = "Regular"
    elif ticket_type == "vip":
        ticket_type = "VIP"
    else:
        messagebox.showerror(
            "Error",
            "Invalid ticket type"
        )
        return

    quantity_to_add = simpledialog.askinteger(
        "Add Stock",
        "Enter additional tickets:",
        minvalue=1
    )

    if quantity_to_add is None:
        return

    movies[movie_name][ticket_type] += quantity_to_add

    messagebox.showinfo(
        "Success",
        "Ticket stock updated!"
    )

    admin()


# Add or rename movies
def update_movies():
    choice = messagebox.askyesno(
        "Update Movies",
        "YES = Add a new movie\nNO = Rename a movie"
    )

    if choice:
        movie_name = simpledialog.askstring("Add Movie","Enter new movie name:")

        if movie_name is None:
            return

        movie_name = movie_name.strip()

        if not movie_name:
            messagebox.showerror("Error","Movie name cannot be empty"
            )
            return

        if movie_name in movies:
            messagebox.showerror(
                "Error",
                "Movie already exists"
            )
            return

        movies[movie_name] = {
            "Regular": 30,
            "VIP": 20
        }

        occupied_seats[movie_name] = set()

    else:
        old_name = simpledialog.askstring(
            "Rename Movie",
            "Current movies:\n" + ", ".join(movies.keys())
        )

        if old_name is None:
            return

        old_name = old_name.strip()

        if old_name not in movies:
            messagebox.showerror(
                "Error",
                "Movie not found"
            )
            return

        new_name = simpledialog.askstring(
            "Rename Movie",
            "Enter new movie name:"
        )

        if new_name is None:
            return

        new_name = new_name.strip()

        if not new_name:
            messagebox.showerror(
                "Error",
                "Movie name cannot be empty"
            )
            return

        if new_name in movies:
            messagebox.showerror(
                "Error",
                "Movie already exists"
            )
            return

        movies[new_name] = movies.pop(old_name)
        occupied_seats[new_name] = occupied_seats.pop(old_name)

    messagebox.showinfo("Success","Movie list updated!")
    admin()

# Remove a movie from the system
def remove_movie():
    if not movies:
        messagebox.showerror("Error", "No movies available to remove")
        return

    movie_name = simpledialog.askstring("Remove Movie","Enter the movie name to remove:\n"+ ", ".join(movies.keys()))

    if movie_name is None:
        return

    movie_name = movie_name.strip()
    if movie_name not in movies:
        messagebox.showerror("Error", "Movie not found")
        return

    confirm = messagebox.askyesno("Confirm Removal","Are you sure you want to remove "+ movie_name + "?")
    if confirm:
        del movies[movie_name]
        occupied_seats.pop(movie_name, None)
        messagebox.showinfo("Success",movie_name + " has been removed!")
        admin()

#all list transaction
def view_transactions():
    window = tk.Toplevel(root)
    window.title("All Transactions")
    window.geometry("1100x450")
    tk.Label(window,text="ALL TRANSACTIONS",font=("Arial", 16, "bold")).pack(pady=10)
    columns = ("ID", "Date", "Username", "Movie", "Ticket Type","Quantity", "Seats", "Total", "Payment", "Change")

    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    table = ttk.Treeview(table_frame,columns=columns,show="headings")

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=100, anchor="center")

    table.column("Date", width=145)
    table.column("Movie", width=110)
    table.column("Seats", width=100)

    scrollbar_y = ttk.Scrollbar(table_frame,orient="vertical",command=table.yview)
    scrollbar_x = ttk.Scrollbar(table_frame,orient="horizontal",command=table.xview)
    table.configure(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set)
    table.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

    transactions = get_all_transactions()

    if not transactions:
        messagebox.showinfo("No Transactions","There are no transactions recorded yet.",parent=window)
    else:
        for transaction in transactions:
            table.insert("", "end", values=transaction)
    tk.Button(window,text="Close",command=window.destroy).pack(pady=5)

# Admin panel
def admin():
    clear()
    tk.Label(root,text="ADMIN PANEL",font=("Arial", 20, "bold")).pack(pady=15)

    for movie_name in movies:
        regular = movies[movie_name]["Regular"]
        vip = movies[movie_name]["VIP"]

        tk.Label( root,text=f"{movie_name}\n"f"Regular: {regular} | VIP: {vip}" ).pack(pady=5)
    tk.Label(root,text=f"Total Sales: ₱{sales:.2f}",font=("Arial", 12)).pack(pady=10)
    tk.Label(root,text=f"Total Transactions: {get_transaction_count()}").pack(pady=5)

    button("Add Ticket Stock", add_ticket_quantity)
    button("Update Movies", update_movies)
    button("Remove Movie", remove_movie)
    button("View All Transactions", view_transactions)
    button("Logout", welcome)