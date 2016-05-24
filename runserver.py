from kronos import app
import uuid
app.secret_key = str(uuid.uuid4())
app.debug = True
app.run()
