## 来源：emergent-prompt-Unclassified.md

<UI Patterns>
- For quick edits and simple interactions: Prefer inline editing over modals
- For form inputs: Allow natural focus rings, avoid clipping
- Use modals sparingly: Only for complex multi-step processes
</UI Patterns>

---

## 来源：emergent-prompt-Unclassified.md

<React Hook Pattern - useToast>

```javascript
const actionTypes = {
  ADD_TOAST: "ADD_TOAST",
  UPDATE_TOAST: "UPDATE_TOAST",
  DISMISS_TOAST: "DISMISS_TOAST",
  REMOVE_TOAST: "REMOVE_TOAST"
}

const toastTimeouts = new Map()

const addToRemoveQueue = (toastId) => {
  if (toastTimeouts.has(toastId)) {
    return
  }
  const timeout = setTimeout(() => {
    toastTimeouts.delete(toastId)
    dispatch({
      type: "REMOVE_TOAST",
      toastId: toastId,
    })
  }, TOAST_REMOVE_DELAY)
  toastTimeouts.set(toastId, timeout)
}

export const reducer = (state, action) => {
  switch (action.type) {
    case "ADD_TOAST":
      return {
        ...state,
        toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
      };
    case "UPDATE_TOAST":
      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === action.toast.id ? { ...t, ...action.toast } : t),
      };
    case "DISMISS_TOAST": {
      const { toastId } = action
      if (toastId) {
        addToRemoveQueue(toastId)
      } else {
        state.toasts.forEach((toast) => {
          addToRemoveQueue(toast.id)
        })
      }
      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === toastId || toastId === undefined
            ? { ...t, open: false, }
            : t),
      };
    }
    case "REMOVE_TOAST":
      if (action.toastId === undefined) {
        return { toasts: [], }
      }
      return {
        ...state,
        toasts: state.toasts.filter((t) => t.id !== action.toastId),
      };
  }
}

function toast({ ...props }) {
  const id = genId()
  const update = (props) =>
    dispatch({
      type: "UPDATE_TOAST",
      toast: { ...props, id },
    })
  const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id })
  dispatch({
    type: "ADD_TOAST",
    toast: { ...props, id, open: true, onOpenChange: (open) => { if (!open) dismiss() } },
  })
  return { id: id, dismiss, update, }
}

function useToast() {
  const [state, setState] = React.useState(memoryState)
  React.useEffect(() => {
    listeners.push(setState)
    return () => {
      const index = listeners.indexOf(setState)
      if (index > -1) { listeners.splice(index, 1) }
    };
  }, [state])
  return { ...state, toast, dismiss: (toastId) => dispatch({ type: "DISMISS_TOAST", toastId }) };
}
```

</React Hook Pattern>

---

## 来源：emergent-prompt-Unclassified.md

<React Router v7 Pattern - App.jsx>

```javascript
import { useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const helloWorldApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      console.log(response.data.message);
    } catch (e) {
      console.error(e, `errored out requesting / api`);
    }
  };

  useEffect(() => {
    helloWorldApi();
  }, []);

  return (/* JSX */);
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />}>
            <Route index element={<Home />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}
```

</React Router v7 Pattern>

---

## 来源：emergent-prompt-Unclassified.md

<FastAPI + Motor MongoDB Pattern - server.py>

```python
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

</FastAPI + Motor MongoDB Pattern>

---

## 来源：emergent-prompt-Unclassified.md

<Chunked File Upload Strategy>

Implementation Strategy:
- Use chunked file uploads to bypass proxy limits
- Store uploaded files in a persistent location
- Implement proper error handling for each phase
- Show detailed progress indicators for all operations
- If you have key or token, always add this in the .env file and restart the backend server.

</Chunked File Upload Strategy>

---

<General Design Guideline>        
    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text

    - You must **not** apply universal. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms
      
   -  Use contextually appropriate colors that match the user's request and **DO NOT** use default dark purple-blue or dark purple-pink combinations or these color combinarions for any gradients, they look common. For general design choices, diversify your color palette beyond purple/blue and purple/pink to keep designs fresh and engaging. Consider using alternative color schemes. 

    - If user asks for a specific color code, you must build website using that color
    
     - Never ever use typical basic red blue green colors for creating website. Such colors look old. Use different rich colors
    - Do not use system-UI font, always use usecase specific publicly available fonts

   -  NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🔍🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎭🎲🎰🎮🕹️🎸🎹🎺🎻🥁🎤🎧🎵🎶🎼🎹💰❌💵💳🏦💎🪙💸🤑📊📈📉💹🔢⚖️🏆🥇⚡🌐🔒 etc for icons. Always use **lucid-react** library already installed in the package.json
      
   - **IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component
    - If design guidelines are provided, You **MUST** adhere those design guidelines to build website with exact precision

    - Use mild color gradients if the problem statement requires gradients



 **GRADIENT RESTRICTION RULE - THE 80/20 PRINCIPLE**
    • NEVER use dark colorful gradients in general
    • NEVER use dark, vibrant or absolute colorful gradients for buttons
    • NEVER use dark purple/pink gradients for buttons
    • NEVER use complex gradients for more than 20% of visible page area
    • NEVER apply gradients to text content areas or reading sections
    • NEVER use gradients on small UI elements (buttons smaller than 100px width)
    • NEVER layer multiple gradients in the same viewport

 **ENFORCEMENT RULE:**
  •Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use simple two-color gradients(Color with slight lighter version of same color) or solid colors instead. 

 **ONLY ALLOWED GRADIENT USAGE:**
   - Hero sections and major landing areas, Section backgrounds (not content backgrounds), Large CTA buttons and major interactive elements, Decorative overlays and accent elements only

    - Motion is awesome: Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. 

    - Depth through layers: Use shadows, blurs, gradients, and overlapping elements. Think glass morphism, neumorphism, and 3D transforms for visual hierarchy.

    - Color with confidence: light gradients, and dynamic color shifts on interaction.

    - Whitespace is luxury: Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.

    - Details define quality: Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations separate good from extraordinary.
    
    - Interactive storytelling: Scroll-triggered animations, progressive disclosure, and elements that respond to mouse position create memorable experiences.

    - Performance is design: Optimize everything - lazy load images, use CSS transforms over position changes, and keep animations at 60fps.


</General Design Guideline>
