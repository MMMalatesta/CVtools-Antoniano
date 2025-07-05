import flet as ft
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import os

def main(page: ft.Page):
    page.title = "CVtools"
    page.scroll = "auto"

    # Definitions
    experiences = []
    education = []
    AntonianoLogo = ft.Image(src="images/AntonianoLogo.png", width=200, height=200, fit="contain")  

    # Setup fields and layout
    def update_widths():
        half_width = page.width / 2
        first_name.width = half_width
        last_name.width = half_width
        email.width = half_width
        phone.width = half_width
        tax_code.width = half_width
        objective.width = half_width
        for start, end, role, description in experiences:
            start.width = half_width / 2
            end.width = half_width / 2
            role.width = half_width
            description.width = half_width
        for title, institution, year in education:
            title.width = half_width
            institution.width = half_width
            year.width = half_width

    # Personal data
    first_name = ft.TextField(label="Nome")
    last_name = ft.TextField(label="Cognome")
    email = ft.TextField(label="Email")
    phone = ft.TextField(label="Telefono")
    tax_code = ft.TextField(label="Codice fiscale, permesso di soggiorno, P. IVA", width=200)

    # Objectives
    objective = ft.TextField(label="Obiettivi professionali (max 200 parole)", multiline=True, max_lines=6)

    # Work experiences
    experiences_section = ft.Column()

    def add_experience(e=None):
        start = ft.TextField(label="Da (anno)", width=100)
        end = ft.TextField(label="a (anno)", width=100)
        role = ft.TextField(label="Ruolo", width=200)
        description = ft.TextField(label="Descrizione", multiline=True, width=400)
        experiences.append((start, end, role, description))
        experiences_section.controls.append(ft.Card(content=ft.Container(ft.Column([
            start, end, role, description
        ]), padding=10)))
        update_widths()
        page.update()

    add_experience()

    # Education
    education_section = ft.Column()

    def add_education(e=None):
        title = ft.TextField(label="Titolo di studio", width=200)
        institution = ft.TextField(label="Instituzione", width=200)
        year = ft.TextField(label="Anno", width=100)
        education.append((title, institution, year))
        education_section.controls.append(ft.Card(content=ft.Container(ft.Row([
            title, institution, year
        ]), padding=10)))
        page.update()

    add_education()

    # === Soft skills ===
    soft_skills = ft.TextField(label="Soft Skills", multiline=False)

    # === PDF Function ===
    def generate_pdf(e):
        filename = "CV.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        y = height - 50

        def write(text, spacing=20, bold=False):
            nonlocal y
            if bold:
                c.setFont("Helvetica-Bold", 12)
            else:
                c.setFont("Helvetica", 12)
            c.drawString(50, y, text)
            y -= spacing

        write("Curriculum Vitae", spacing=30, bold=True)
        write(f"Nome: {first_name.value}")
        write(f"Cognome: {last_name.value}")
        write(f"Email: {email.value}")
        write(f"Telefono: {phone.value}")
        write(f"Codice fiscale, permesso di soggiorno, P. IVA: {tax_code.value}")

        write("Obiettivi professionali:", spacing=25, bold=True)
        for line in objective.value.split("\n"):
            write(line, spacing=15)

        write("Esperienze lavorative:", spacing=25, bold=True)
        for start, end, role, description in experiences:
            write(f"{start.value} - {end.value}: {role.value}")
            for line in description.value.split("\n"):
                write(f"  {line}", spacing=15)

        write("Educazione:", spacing=25, bold=True)
        for title, institution, year in education:
            write(f"{year.value} - {title.value} ({institution.value})")

        write("Soft Skills:", spacing=25, bold=True)
        for skill in soft_skills.value.split(","):
            write(f"- {skill.strip()}", spacing=15)

        c.save()
        page.dialog = ft.AlertDialog(title=ft.Text("PDF Generated!"), content=ft.Text(f"Saved as {filename}"))
        page.dialog.open = True
        page.update()

    # === Layout with Cards ===
    page.add(
        ft.Row([
            ft.Column([
                ft.Text("Crea il tuo CV con Antoniano!", size=24, weight="bold"),
                ft.Card(content=ft.Container(ft.Column([
                    ft.Text("Dati personali", size=18, weight="bold"),
                    first_name, last_name, email, phone, tax_code
                ]), padding=10)),

                ft.Card(content=ft.Container(ft.Column([
                    ft.Text("Obiettivi professionali", size=18, weight="bold"),
                    objective
                ]), padding=10)),

                ft.Card(content=ft.Container(ft.Column([
                    ft.Text("Esperienze di lavoro", size=18, weight="bold"),
                    experiences_section,
                    ft.TextButton("+ Aggiungi esperienza", on_click=add_experience)
                ]), padding=10)),

                ft.Card(content=ft.Container(ft.Column([
                    ft.Text("Educazione", size=18, weight="bold"),
                    education_section,
                    ft.TextButton("+ Aggiungi titolo di studi", on_click=add_education)
                ]), padding=10)),

                ft.Card(content=ft.Container(ft.Column([
                    ft.Text("Soft Skills", size=18, weight="bold"),
                    soft_skills
                ]), padding=10)),

                ft.ElevatedButton("Genera PDF", on_click=generate_pdf)
            ], expand=2),

        ft.Column([
            ft.Container(
                    content=AntonianoLogo,
                    alignment=ft.alignment.top_center,  # Align logo to the top-right
                    padding=10
                ),
            ft.Container(
                    content=ft.Text("Benvenuto al laboratorio di CV", size=16, weight="bold"),
                    alignment=ft.alignment.top_center,  # Align logo to the top-right
                    padding=10
                ),
            
            ], 
            expand=1, 
            alignment=ft.MainAxisAlignment.START, 
            horizontal_alignment=ft.CrossAxisAlignment.END
            ) 
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN)  # ⬅ This spaces left and right columns)
    )

ft.app(target=main)