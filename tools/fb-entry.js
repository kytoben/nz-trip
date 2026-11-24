export {initializeApp} from "firebase/app";
export {getAuth, onAuthStateChanged, signInWithEmailAndPassword, setPersistence, browserLocalPersistence, signOut} from "firebase/auth";
export {initializeFirestore, persistentLocalCache, persistentMultipleTabManager, doc, collection, onSnapshot, setDoc, deleteDoc} from "firebase/firestore";
