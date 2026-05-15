import os

SUSPICIOUS_EXTENSIONS = [
    ".exe",
    ".scr",
    ".js",
    ".vbs",
    ".bat",
    ".cmd",
    ".ps1",
    ".jar",
    ".msi"
]

OFFICE_MACRO_EXTENSIONS = [
    ".docm",
    ".xlsm",
    ".pptm"
]

ARCHIVE_EXTENSIONS = [
    ".zip",
    ".rar",
    ".7z"
]


def detect_double_extension(filename):

    parts = filename.lower().split(".")

    if len(parts) > 2:

        return True

    return False


def analyze_attachments(attachments):

    results = {
        "suspicious_files": [],
        "macro_files": [],
        "archives": [],
        "double_extensions": [],
        "reasons": []
    }

    if not attachments:

        return results

    for file in attachments:

        filename = file.lower()

        # -------------------------
        # Suspicious executables
        # -------------------------
        for ext in SUSPICIOUS_EXTENSIONS:

            if filename.endswith(ext):

                results["suspicious_files"].append(file)

                results["reasons"].append(
                    f"Suspicious executable detected: {file}"
                )

        # -------------------------
        # Macro files
        # -------------------------
        for ext in OFFICE_MACRO_EXTENSIONS:

            if filename.endswith(ext):

                results["macro_files"].append(file)

                results["reasons"].append(
                    f"Office macro file detected: {file}"
                )

        # -------------------------
        # Archives
        # -------------------------
        for ext in ARCHIVE_EXTENSIONS:

            if filename.endswith(ext):

                results["archives"].append(file)

                results["reasons"].append(
                    f"Archive file detected: {file}"
                )

        # -------------------------
        # Double extension attack
        # -------------------------
        if detect_double_extension(filename):

            results["double_extensions"].append(file)

            results["reasons"].append(
                f"Possible double extension attack: {file}"
            )

    return results