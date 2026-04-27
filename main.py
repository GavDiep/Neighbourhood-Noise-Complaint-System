# ============================================================
#  THE NEIGHBOURHOOD NOISE COMPLAINT SYSTEM
#  CS30 — Object-Oriented Programming 2 (CSE3130)
#  Divine Mustafa | Gavin Diep | Yuvraj Sond | Sebastian Villanueva
# ============================================================
import random

# ── CONSTANTS ────────────────────────────────────────────────
COMPLAINT_REASONS = [
    "Fired a hose at me while I was walking my dog",
    "Their dogs favourite toilet is apparently my front yard",
    "Doesn't know how to use driveways, his car is always in my lawn",
    "Set up a telescope to 'view the stars' (it's always pointed directly at my bedroom)",
    "Ever since he bought his first motorcycle, it's been hard to imagine any sounds besides the revving of his engine",
    "Bought a million-lumen flashlight and now thinks he's the sun",
    "Backyard fire pit that has, legally speaking, no upper size limit apparently",
    "Bought a new gaming set up, I've never heard curse words so creative before",
    "Set off the brightest firework I've ever seen, and then had the audacity to come over to my house after and ask if I enjoyed the 'retina wrecker'.",
    "Left their bathroom window open after leaving what one could only assume is the world's most pungent substance.",
    "Consistently leaving their hose on after use, which has led to the flooding of my lawn.",
    "Purposely leaving nails in the road as a way to 'deter pests', this has only resulted in the entire neighbourhood getting flats.",
    "Cooking rancid meals and leaving them out to cool on their window, poisoning the air.",
    "'Accidently' mixed ammonia and bleach together and caused poison control to be called to clean out what could only be described as a first world war gas attack.",
]

NOISE_COMPLAINT_REASONS = [
    "Estimated 75dB. Yelling while playing video games at 8:00PM at night, owls have requested a ban on video games in the neighbourhood",
    "Estimated 80dB. Listening to radio too loud at 7:00AM in the morning, Birds have ordered earplugs.",
    "Estimated 100dB. Tuning guitar at odd hours in the day, disturbing my evening nap.",
    "Estimated 110dB. Playing loud electronic music too early in the morning, summoned a flash mob in the neighbourhood that blocks traffic",
    "Estimated 130dB. Band is playing at their home in the middle of the night, causes local wildlife to gather outside their home for a concert.",
]


# ── FUNCTIONS ────────────────────────────────────────────────
def create_reference_number(all_complaints):
    """
    Creates a unique identifier for a complaint by looping through all existing formal complaints

    Parameters:
        all_complaints (array): A list of every complaint
    """
    number = 0
    for complaint in all_complaints:
        if hasattr(complaint, "reference_number"):
            ref_num = int(complaint.reference_number.split("-")[1])
            if number < ref_num:
                number = ref_num + 1
            if number == ref_num:
                number += 1

    return f"FC-{number}"


def get_complaint(decibel_level=None):
    """
    Gets a random complaint from the COMPLAINT_REASONS list

    Returns:
        complaint (string): A string from the COMPLAINT_REASONS list
    """
    length = len(COMPLAINT_REASONS) - 1
    normal_reason = COMPLAINT_REASONS[random.randint(0, length)]

    complaint = decibel_level if decibel_level else normal_reason
    return complaint


# ── CLASSES ────────────────────────────────────────────────
class Complaint:
    """
    Represents a single noise complaint filed by one neighbour against another.

    Attributes:
        against (str): Name of the accused
        reason (str): The specific offence
        severity (int): 1–5. 1 = mild irritation. 5 = I am calling a lawyer.
        escalated (bool): Whether this has been escalated to the neighbourhood council
        day (int): Which day of the simulation this was filed
    """

    def __init__(self, against, reason, severity, escalated, day):
        """Initializes the complaints attributes"""
        self.against = against
        self.reason = reason
        self.severity = max(1, min(5, severity))
        self.escalated = escalated
        self.day = day

    def __str__(self):
        """Returns a summary of the complaint"""
        summary = f"\nDay: {self.day} | Against: {self.against.name} \nReason: {self.reason} \nSeverity: {self.severity} | Escalated: {self.escalated}"
        return summary

    def escalate(self):
        """Sets the escalated attribute to true"""
        self.escalated = True

    def is_serious(self):
        """Determines if the complaints severity is high enough to be considered significant"""
        return self.severity >= 4


class FormalComplaint(Complaint):
    """
    Represents a formal complaint filed by a neighbour.

    New Attributes:
        reference_number (str): Auto-generated unique ID
        response (str): Council's response. Default: 'Pending'
    """

    def __init__(
        self,
        against,
        reason,
        severity,
        escalated,
        day,
        neighbourhood,
        response="Pending",
    ):
        """initializes the formal complaint attributes"""
        super().__init__(against, reason, severity, escalated, day)
        self.response = response

        # gathers every complaint to create a reference number
        all_complaints = []

        for n in neighbourhood:
            for g in n.grievances:
                all_complaints.append(g)

        self.reference_number = create_reference_number(all_complaints)

    def __str__(self):
        """Returns a summary of the formal complaint, including the reference number and response"""
        summary = f"Day {self.day} | Reference {self.reference_number} \nAgainst: {self.against.name} \nReason: {self.reason} \nSeverity: {self.severity} | Escalated: {self.escalated} | Response: {self.response}"
        return summary

    def resolve(self, outcome):
        """Sets the response to equal to the outcome"""
        self.response = outcome


class Neighbour:
    """
    Neighbour class used to create neighbours
       Attributes:
    name: The neighbour's name
    address: The neighbour's address
    noise_level: How loud the neighbour is (int 1-5)
    tolerance: How tolerable the neighbour is (int 1-10)
    complaints_recieved: How many complaints they recieve over the course of the week
    (pre-set value of 0)
    score: Their insufferability score (starting value of 0)
    allies: The neighbour's allies
    feuds: The people/families the neighbour is on bad terms with
    grievances: an array of the neighbour's complaints, empty to start
    """

    def __init__(
        self,
        name,
        address,
        noise_level,
        tolerance,
        allies,
        feuds,
        complaints_received=0,
        score=0,
        grievances=None,
    ):
        self.name = name
        self.address = address
        self.noise_level = max(0, min(10, noise_level))
        self.tolerance = tolerance
        self.allies = allies
        self.feuds = feuds
        self.complaints_received = complaints_received

        self.grievances = [] if grievances == None else grievances

        self.score = max(
            0, (self.noise_level * 2) + (self.complaints_received * 3) - self.tolerance
        )

    def __str__(self):
        """Prints all relevant information for a neighbour object in a readable way"""
        grievances_str = (
            "\n  ".join(str(g) for g in self.grievances) if self.grievances else "None"
        )
        return (
            f"Name: {self.name}\n"
            f"Address: {self.address}\n"
            f"Noise Level: {self.noise_level}\n"
            f"Tolerance Level: {self.tolerance}\n"
            f"Complaints Recieved: {self.complaints_received}\n"
            f"Score: {self.score}\n"
            f"Allies: {', '.join(self.allies)}\n"
            f"Feuds: {', '.join(self.feuds)}\n"
            f"Grievances: {grievances_str}\n"
        )

    def get_target(self, neighbourhood):
        """Finds a target for a complaint from the 'neighbourhood' array, finding a new target in the scenario that they choose themselves"""
        index = random.randint(0, 5)
        target = neighbourhood[index]
        target_name = target.name

        while target_name == self.name or target_name in self.allies:
            index = random.randint(0, 5)
            target = neighbourhood[index]
            target_name = target.name

        return target

    def file_complaint(self, target, severity, escalated, day=0):
        """
        File a Complaint against the target Neighbour.
        Creates a Complaint object, appends to self.grievances,
        and increments target.complaints_received.
        Prints a formatted message.

        Parameters:
            target (Neighbour): The accused
            reason (str): The offence
            severity (int): 1–5
            escalated: whether or not the complaint has a severity > 3
            day (int): Simulation day
        """
        # if the target is a noisy neighbour, the complaint reason will be a noisy complaint
        reason = (
            get_complaint(target.decibel_estimate())
            if hasattr(target, "noise_source")
            else get_complaint()
        )
        grievance = Complaint(target, reason, severity, escalated, day)

        # duplicate prevention
        for g in self.grievances:
            while (
                g.against.name == grievance.against.name
                and g.reason == grievance.reason
            ):
                reason = (
                    get_complaint(target.decibel_estimate())
                    if hasattr(target, "noise_source")
                    else get_complaint()
                )
                grievance = Complaint(target, reason, severity, escalated, day)

        print(f'"{reason}"\n')

        target.complaints_received += 1
        target.score = (
            (target.noise_level * 2)
            + (target.complaints_received * 3)
            - target.tolerance
        )
        self.grievances.append(grievance)

    def get_escalated_complaints(self):
        """Returns a list of complaints in which the 'escalated' attribute is True"""
        escalated_issues = []
        for grievance in self.grievances:
            if grievance.escalated == True:
                escalated_issues.append(grievance)
        return escalated_issues


class NoisyNeighbour(Neighbour):
    """
    A subclass of the neighbour class

    Attributes:
    noise_source - describes the source of their noise

    Overridden Methods:
    file_complaint() - increases the severity of complaints against them by 1
    """

    def __init__(
        self,
        name,
        address,
        noise_level,
        noise_source,
        tolerance,
        allies,
        feuds,
        complaints_received=0,
        score=0,
        grievances=None,
    ):
        super().__init__(
            name,
            address,
            noise_level,
            tolerance,
            allies,
            feuds,
            complaints_received,
            score,
            grievances,
        )
        if self.noise_level < 7:
            raise Exception(
                "Noise level must be 7 or higher to qualify as a noisy neighbour"
            )
        self.noise_source = noise_source

    def file_complaint(self, target, severity, escalated, day=0):
        """Takes the 'file_complaint' method from the neighbour parent class and makes it automatically add 1 to the severity attribute, with the cap still being 5"""

        reason = (
            get_complaint(target.decibel_estimate())
            if hasattr(target, "noise_source")
            else get_complaint()
        )
        grievance = Complaint(target, reason, severity + 1, escalated, day)

        # duplicate prevention
        for g in self.grievances:
            while (
                g.against.name == grievance.against.name
                and g.reason == grievance.reason
            ):
                reason = (
get_complaint(target.decibel_estimate())
           	if hasattr(target, "noise_source")
           	else get_complaint()
         )
                grievance = Complaint(target, reason, severity, escalated, day)

        print(f'"{reason}"\n')

        if severity > 5:
            severity = 5
        target.complaints_received += 1
        target.score = (
            (target.noise_level * 2)
            + (target.complaints_received * 3)
            - target.tolerance
        )
        self.grievances.append(grievance)

        return reason

    def decibel_estimate(self):
        """Returns a noise complaint string from the 'NOISE_COMPLAINT_REASONS' array based on the neighbour's noise level"""
        estimate = 0
        if self.noise_level == 8:
            estimate = random.randint(0, 1)
        elif self.noise_level == 9:
            estimate = random.randint(2, 3)
        elif self.noise_level == 10:
            estimate = 4
        decibel_level = NOISE_COMPLAINT_REASONS[estimate]
        return decibel_level


class CouncilMember(Neighbour):
    """
    A neighbour who sits on the neighbourhood council and can formally arbitrate disputes.

    Additional Attributes:
        jurisdiction (list): House numbers (ints) this member oversees
        rulings (list): Strings recording past decisions
    """

    def __init__(
        self,
        name,
        address,
        noise_level,
        tolerance,
        allies,
        feuds,
        jurisdiction,  # new
        rulings=[],  # new
        complaints_received=0,
        score=0,
        grievances=None,
    ):
        super().__init__(
            name,
            address,
            noise_level,
            tolerance,
            allies,
            feuds,
            complaints_received,
            score,
            grievances,
        )
        self.jurisdiction = jurisdiction
        self.rulings = rulings

    def arbitrate(self, complaint, filer, neighbourhood):
        """
        Formally arbitrate a complaint.

        If the complaint's target lives in self.jurisdiction:
            - Create a FormalComplaint from the complaint's data
            - Replace the original complaint in filer.grievances with the FormalComplaint
            - Add a ruling string to self.rulings
            - Print a formal announcement
            - Return the FormalComplaint

        If the target is NOT in jurisdiction:
            - Raise a ValueError with a sassy message about jurisdiction

        Parameters:
            complaint (Complaint): The complaint to arbitrate
            filer (Neighbour): The neighbour who filed it
            neighbourhood (Street): A list of every neighbour

        Returns:
            FormalComplaint

        Raises:
            ValueError: If target is outside jurisdiction (must be as sassy as posssible)
        """

        if complaint.against.address in self.jurisdiction:
            formal_complaint = FormalComplaint(
                complaint.against,
                complaint.reason,
                complaint.severity,
                complaint.escalated,
                complaint.day,
                neighbourhood,
            )
            formal_complaint.escalated = True
            index = next(
                i
                for i, obj in enumerate(filer.grievances)
                if obj.against.name == complaint.against.name
                and obj.reason == complaint.reason
                and obj.day == complaint.day
            )
            filer.grievances[index] = formal_complaint
            self.rulings.append(
                f"Arbitrated a complaint from {filer.name} which was targeted towards {complaint.against.name}."
            )
            print(formal_complaint.reference_number)
            print(
                f"A complaint from {filer.name} targeted towards {complaint.against.name} has been arbitrated."
            )
            return formal_complaint
        else:
            try:
                raise ValueError(
                    f"Um, actually, the address, {filer.address}, is outside of the jurisdiction of {self.name}, your going to need to find a different council member to arbitrate this complaint."
                )
            except ValueError as e:
                print(e)


class Street:
    """
    Manages the entire neighbourhood — a collection of Neighbour objects.

    Attributes:
        name (str): Name of the street
        neighbours (list): List of Neighbour objects
    """

    def __init__(self, name):
        """Initializes name and a empty neighbourhood list"""
        self.name = name
        self.neighbourhood = []

    def add_neighbour(self, neighbour):
        """Adds a neighbour to the list"""
        self.neighbourhood.append(neighbour)

    def get_neighbour(self, name):
        """Iterates through the list"""
        for neighbour in self.neighbourhood:
            """Returns the name of the neighbour if found"""
            if neighbour.name == name:
                return neighbour.name

    def remove_neighbour(self, name):
        """Iterates through the list"""
        for neighbour in self.neighbourhood:
            """Removes the neighbour from the list if found"""
            if neighbour.name == name:
                self.neighbourhood.remove(neighbour)

    def most_insufferable(self):
        """
        Find the highest insufferability score by calling the
        insufferability_score() method
        """

        highest_insufferability = 0

        highest = max(self.neighbourhood, key=lambda x: x.score)
        return highest

    def feuding_pairs(self):
        """
        Return a list of tuples (neighbour_a, neighbour_b) for every mutual feud.
        A feud is mutual when A has B's name in feuds AND B has A's name in feuds.
        Each pair should appear only once.

        Returns:
            list of tuples
        """

        # Initalize feuding neighbours list, and neighbour A and B
        # A is the neighbour feuding with B
        neighbour_a = ""
        neighbour_b = ""
        feuding_neighbours = []

        # Iterate through the neighbourhood list
        for i in self.neighbourhood:
            # Checks if the neighbour has any feuds
            if i.feuds:
                # Store neighbour A's name
                neighbour_a = i.name

                # Iterate through the neighbour's feuds
                for feud in i.feuds:
                    # Store neighbour B's name'
                    neighbour_b = feud

                    # Iterate the neighbourhood list again
                    for neighbour in self.neighbourhood:
                        # And find the feuded neighbour
                        if neighbour.name == neighbour_b:
                            # Also check if neighbour B has any feuds
                            if neighbour.feuds:
                                # check if neighbour A is in neighbour B's feuds
                                if neighbour_a in neighbour.feuds:
                                    # Add the pair to the list as a tuple
                                    feuding_neighbours.append(
                                        (neighbour_a, neighbour_b)
                                    )

        # Organize the list to remove duplicates
        # Iterate the feuding neighbours list
        for pair in feuding_neighbours:
            # Replace the variables with the pair names
            neighbour_a = pair[0]
            neighbour_b = pair[1]

            # Checks for flipped duplicate pairs in the list
            if (neighbour_b, neighbour_a) in feuding_neighbours:
                # Remove the duplicate pair
                feuding_neighbours.remove((neighbour_b, neighbour_a))

        # Return the list of feuding pairs
        return feuding_neighbours

    def sort_by_noise(self):
        """
        Return a new list sorted by noise_level, highest first.
        Use sorted() with a lambda key. Do NOT sort in place.

        Returns:
            list
        """
        noise_list = sorted(
            self.neighbourhood, key=lambda x: x.noise_level, reverse=True
        )
        return noise_list

    def sort_by_insufferability(self):
        """
        Return a new list sorted by insufferability.

        Returns:
            list
        """
        insufferability_list = sorted(
            self.neighbourhood, key=lambda x: x.score, reverse=True
        )
        return insufferability_list

    def escalate_all(self):
        """
        Check all grievances across all neighbours.
        Any complaint that is_serious() AND the target's noise_level >= 7
        gets escalated via complaint.escalate().

        Returns:
            int: Number of complaints escalated
        """
        complaints_escalated = 0
        for neighbour in self.neighbourhood:
            for complaint in neighbour.grievances:
                if complaint.is_serious() and complaint.against.noise_level >= 7:
                    complaint.escalate()
                    complaints_escalated += 1

        return complaints_escalated

    def run_week(self):
        """
        Simulate 7 days on the street.

        Each day: for each Neighbour, if tolerance <= 3 AND any neighbour
        in their feuds list has noise_level >= 6, call self.file_complaint()
        automatically with a random reason.

        KEY REQUIREMENT: Do NOT use isinstance() checks to decide which
        file_complaint() to call. Just call neighbour.file_complaint() and
        let polymorphism handle the rest.

        After 7 days: call escalate_all(), then full_report().
        """

        # stores the indexes of the council members
        council_indexes = []
        for i, n in enumerate(self.neighbourhood):
            if hasattr(n, "jurisdiction"):
                council_indexes.append(i)

        # 7 days loop
        for i in range(1, 8):
            # Title message
            day_title = f"Day: {i}"

            print(f"{'=' * 75}")
            print(day_title.center(75))  # Center the day
            print(f"{'=' * 75}\n")

            # Loops through every neighbour
            for neighbour in self.neighbourhood:
                # Loops through the neighbour's feuds
                for name in neighbour.feuds:
                    person = next(n for n in self.neighbourhood if n.name == name)
                    chance_to_file = random.randint(
                        1, 100
                    )

                    if (
                        person.noise_level >= 6
                        and neighbour.tolerance <= 3
                        and chance_to_file > 25 # 50% chance to file a complaint
                    ):
                        print(
                            f"{neighbour.name} filed a complaint against {person.name}."
                        )
                        severity = random.randint(1, 5)
                        neighbour.file_complaint(person, severity, False, i)

                # Loops through the neigbour's complaints to arbitrate or resolve them
                for complaint in neighbour.grievances:
                    isFormal = hasattr(complaint, "reference_number")

                    # Waits a day before arbitrating and checks if the severity is high enough
                    if not isFormal and complaint.day < i and complaint.severity > 3:
                        for i in council_indexes:
                            member = self.neighbourhood[i]
                            if complaint.against.address in member.jurisdiction:
                                member.arbitrate(
                                    complaint, neighbour, self.neighbourhood
                                )
                                print("")

                    # resolves the formal complaint
                    elif isFormal and complaint.day < i - 2:
                        if complaint.response != "Resolved":
                            outcomes = ["Pending", "Lightened", "Worsened", "Resolved"]
                            outcome = outcomes[random.randint(0, 2)]
                            complaint.resolve("outcome")

                            if outcome != "Pending":
                                print(complaint.reference_number)

                            if outcome == "Lightened":
                                print(
                                    f"A complaint from {neighbour.name} targeted towards {complaint.against.name} is cooling down.\n"
                                )
                            elif outcome == "Worsened":
                                print(
                                    f"A complaint from {neighbour.name} targeted towards {complaint.against.name} erupted in violence.\n"
                                )
                            elif outcome == "Resolved":
                                print(
                                    f"A complaint from {neighbour.name} targeted towards {complaint.against.name} has been resolved.\n"
                                )

            print("\n\n")


        # calls the final two methods to finish up the run
        self.escalate_all()
        self.full_report()

    def full_report(self):
        """
        Print the complete street report:
        - Street name header
        - All neighbours ranked by insufferability
        - Total complaints filed and received
        - Any escalated/formal complaints
        - Declaration of Most Insufferable Resident
        """

        # Header
        header = f"{self.name.upper()} -- WEEKLY INCIDENT REPORT"

        print(f"\n{'=' * 75}")
        print(header.center(75))  # Center the header
        print(f"{'=' * 75}\n")

        # Insufferbility Ranking
        ranking_title = "INSUFFERABILITY RANKING"
        print(f"{ranking_title.center(75, '-')}\n")

        insufferable_ranking = self.sort_by_insufferability()
        for rank in insufferable_ranking:
            print(f"{rank.name}: {rank.score}")

        # Total Complaints Filed and Received
        print(f"\n{'TOTAL NUMBER OF COMPLAINTS THIS WEEK'.center(75, '-')}")

        total_complaints = 0
        for neighbor in self.neighbourhood:
            # Add the number of grievances
            total_complaints += len(neighbor.grievances)
            # Add the number of complaints received
            total_complaints += neighbor.complaints_received

        print(f"\n{total_complaints} Complaints Filed And Received\n")

        # Display every escalated and formal complaint
        print(f"ESCALATED AND FORMAL COMPLAINTS".center(75, "-"))

        # Iterate the neighbourhood list
        for neighbor in self.neighbourhood:
            # Check if the resident has any complaints
            if neighbor.grievances:
                # Iterate through the list of complaints
                for complaint in neighbor.grievances:
                    # Check if the complaint has escalated
                    if complaint.escalated:
                        print(f"\n{complaint}\n")

        # Declare the most insufferable resident
        # Get the most insufferable resident
        most_insufferable_resident = self.most_insufferable()
        declaration = f"{most_insufferable_resident.name.upper()} IS THE MOST INSUFFERABLE RESIDENT OF {self.name.upper()}"

        print(f"\n{'=' * 75}")
        print(declaration.center(75))  # Center the declaration
        print(f"{'=' * 75}\n")

        # End Report
        print(f"END OF WEEKLY INCIDENT REPORT".center(75))


# ── TESTING ────────────────────────────────────────────────
my_street = Street("maplewood Crescent")

# Neighbours (name, address, noise_level, tolerance, allies, feuds, complaints_received=0, score=0, grievances=[])
my_street.add_neighbour(
    Neighbour(
        "John Marston", "2 Maplewood Crescent", 3, 2, ["Tony Blair"], ["Paul Stanley"]
    )
)
my_street.add_neighbour(
    Neighbour(
        "Steve Angello", "7 Maplewood Crescent", 6, 2, ["Axel Hedfor"], ["Tony Blair"]
    )
)


# Noisy Neighbours (name, address, noise_level, noise_source, tolerance, allies, feuds, complaints_received=0, score=0, grievances=[])
my_street.add_neighbour(
    NoisyNeighbour(
        "David Grohl",
        "5 Maplewood Crescent",
        8,
        "Guitar",
        9,
        ["Paul Stanley", "Axel Hedfor", "Steve Angello"],
        [],
    )
)
my_street.add_neighbour(
    NoisyNeighbour(
        "Paul Stanley",
        "4 Maplewood Crescent",
        9,
        "Loud Vocals",
        2,
        ["David Grohl"],
        ["Axel Hedfor", "Tony Blair"],
    )
)
my_street.add_neighbour(
    NoisyNeighbour(
        "Axel Hedfor",
        "8 Maplewood Crescent",
        8,
        "Speakers",
        7,
        ["Steve Angello"],
        ["Tony Blair"],
    )
)


# Council Members (name, address, noise_level, tolerance, allies, feuds, jurisdiction, rulings=[], complaints_received=0, score=0, grievances=[])
my_street.add_neighbour(
    CouncilMember(
        "Tony Blair",
        "3 Maplewood Crescent",
        4,
        1,
        ["John Marston"],
        ["Paul Stanley", "Steve Angello"],
        [
            "3 Maplewood Crescent",
            "2 Maplewood Crescent",
            "5 Maplewood Crescent",
            "7 Maplewood Crescent",
        ],
    )
)
my_street.add_neighbour(
    CouncilMember(
        "Divine Mustafa",
        "10 Maplewood Crescent",
        1,
        10,
        ["Steve Angello"],
        ["Axel Hedfor", "Tony Blair"],
        ["10 Maplewood Crescent", "4 Maplewood Crescent", "8 Maplewood Crescent"],
    )
)


my_street.run_week()
