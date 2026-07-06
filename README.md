# EventHub — Sistema di Gestione Eventi

**Studente:** Tommaso Sottili
**Esame:** Produzione e Progettazione Multimediale (PPM) — modulo "Backend con Django"
**Tipo di progetto:** Full-Stack Web Application
**Framework:** Django 5.2 (Python 3.12)

---

## Descrizione e scopo

EventHub è un'applicazione web per la gestione di eventi. Permette agli utenti di
registrarsi, agli **organizzatori** di creare e gestire i propri eventi, e ai
**partecipanti** di iscriversi agli eventi disponibili. Il sito è interamente
navigabile dal browser e mostra pagine, menu e pulsanti diversi a seconda del
ruolo dell'utente.

Il progetto è realizzato come applicazione full-stack con Django (Model-View-Template),
autenticazione integrata, ruoli basati su Gruppi e permessi applicati nel codice.

---

## Funzionalità per ruolo

**Visitatore (non autenticato)**
- Consulta l'elenco degli eventi e il dettaglio di ciascun evento
- Si registra e accede al sito

**Partecipante (Attendee)**
- Tutto quanto sopra
- Si iscrive e annulla l'iscrizione agli eventi
- Consulta la pagina "Le mie registrazioni"

**Organizzatore (Organizer)**
- Crea, modifica ed elimina i **propri** eventi (CRUD completo)
- Consulta la lista dei partecipanti dei propri eventi
- Consulta la pagina "I miei eventi"
- Può anche iscriversi come partecipante agli eventi organizzati da altri

**Amministratore (superuser)**
- Accede al pannello di amministrazione di Django (`/admin/`) per gestire utenti,
  gruppi, eventi e iscrizioni

---

## Scelte tecniche (mappa dei requisiti)

- **Struttura modulare:** due app Django, `accounts` (utenti e autenticazione) ed `events` (eventi e iscrizioni)
- **Modello dati relazionale:** due relazioni `ForeignKey` — `Event.organizer` (utente → eventi) e il modello-ponte `Registration` (utente ↔ evento)
- **Custom user model:** `accounts.CustomUser` che estende `AbstractUser`
- **Ruoli e permessi:** due Gruppi (`Organizer`, `Attendee`) applicati nel codice con i mixin `LoginRequiredMixin` e `UserPassesTestMixin` e riflessi nell'interfaccia
- **Class-based / generic views:** `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`
- **Validazione input:** `ModelForm` con campi espliciti e messaggi d'errore
- **CRUD completo** sugli eventi, secondo i permessi
- **Dati demo** inclusi nel database SQLite pre-popolato

---

## Installazione ed esecuzione in locale

```bash
# 1. Clona la repository
git clone <URL-della-repo>
cd <cartella-del-progetto>

# 2. Crea e attiva un ambiente virtuale
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Avvia il server di sviluppo
python manage.py runserver
```

Apri poi il browser su **http://127.0.0.1:8000/**.

Il database `db.sqlite3` è **già incluso nella repository e popolato** con i dati
demo: non è necessario eseguire migrazioni o caricare fixtures per provarlo in locale.

> Se si volesse ricreare il database da zero:
> `python manage.py migrate` seguito da `python manage.py loaddata demo`.

---

## Database e dati demo

- **File database:** `db.sqlite3` (incluso nella repo, già popolato)
- **Fixture sorgente dei dati demo:** `events/fixtures/demo.json`

Il database contiene account per ogni ruolo, alcuni eventi realistici e diverse
iscrizioni, sufficienti a testare l'intero flusso.

---

## Account demo

| Username         | Password         | Ruolo                       |
|------------------|------------------|-----------------------------|
| `admin_demo`     | `admin12345`     | Amministratore (superuser)  |
| `organizer_demo` | `organizer12345` | Organizzatore               |
| `attendee_demo`  | `attendee12345`  | Partecipante                |

*(Credenziali fittizie, valide solo a scopo di valutazione.)*

---

## Link al deploy online

**[DA INSERIRE DOPO IL DEPLOY SU RAILWAY]**

La versione online permette di accedere con gli account demo e testare l'intero
workflow dal browser, senza installare nulla.

---

## Scenario di test dal browser

1. Apri il sito (in locale o tramite il link online) e osserva l'elenco degli eventi.
2. Accedi come **`organizer_demo`**: crea un nuovo evento, modificane uno esistente
   e apri la lista dei suoi partecipanti.
3. Esci e accedi come **`attendee_demo`**: apri un evento e **iscriviti**, poi
   controlla la pagina "Le mie registrazioni".
4. **Prova un'azione vietata:** sempre come `attendee_demo`, scrivi manualmente
   nella barra dell'indirizzo l'URL di modifica di un evento non tuo, ad esempio
   `/event/1/edit/` → il sito risponde con una pagina **403 (Accesso negato)**,
   perché la modifica è riservata all'organizzatore dell'evento.
5. Esci e accedi come **`admin_demo`**: apri `/admin/` e verifica la gestione di
   utenti, gruppi, eventi e iscrizioni.

---

## Tecnologie utilizzate

Django · Django Template Language · Bootstrap 5 · SQLite (locale) · PostgreSQL
(produzione) · WhiteNoise · Gunicorn · deploy su Railway.
