# MĪZĀN AL-ḤADĪTH — REST API ENDPOINT REFERENCE

**Document Identifier:** `docs/api/endpoint-reference.md`  
**Total Endpoints Documented:** 85 Paths (95 operations)  
**OpenAPI Version:** 3.1.0  

---

## 1. Master Endpoint Index

| Method | Endpoint Path | Summary / Purpose | Category |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/ask` | Ask Hadith Query | Ask Mīzān |
| `GET` | `/api/ask/conversations/{conversation_id}` | Get Conversation | Ask Mīzān |
| `POST` | `/api/ask/feedback` | Submit Feedback | Ask Mīzān |
| `GET` | `/api/ask/health` | Ask Health | Ask Mīzān |
| `POST` | `/api/ask/stream` | Ask Hadith Query Stream | Ask Mīzān |
| `GET` | `/api/annotations` | Get Scholarly Annotations | General |
| `POST` | `/api/annotations` | Create Scholarly Annotation | General |
| `GET` | `/api/books` | Get Books | General |
| `GET` | `/api/books/{book_id}` | Get Book | General |
| `GET` | `/api/books/{book_id}/hadith/by-number/{hadith_number}` | Get Book Hadith By Number | General |
| `GET` | `/api/books/{book_id}/hadith/{hadith_number}` | Get Book Hadith By Number | General |
| `GET` | `/api/books/{book_id}/hadiths` | Get Book Hadiths | General |
| `GET` | `/api/books/{book_id}/hadiths/by-number/{hadith_number}` | Get Book Hadith By Number | General |
| `GET` | `/api/books/{book_id}/hadiths/search` | Search Book Hadiths | General |
| `GET` | `/api/books/{book_id}/numbering-options` | Get Book Numbering Options | General |
| `GET` | `/api/books/{book_id}/resolve-number` | Resolve Book Number Endpoint | General |
| `GET` | `/api/books/{book_id}/search` | Search Book Hadiths | General |
| `GET` | `/api/books/{book_id}/search/en` | Search Book English | General |
| `GET` | `/api/diagnostics/db-lifecycle` | Get Db Lifecycle Diagnostics | General |
| `GET` | `/api/diagnostics/hybrid-shadow` | Get Hybrid Shadow Diagnostics | General |
| `GET` | `/api/english-search/coverage` | English Search Coverage | General |
| `GET` | `/api/hadith-visualization/hadith/{hadith_id}` | Get Hadith Visualization Detail | General |
| `GET` | `/api/hadith-visualization/network` | Get Hadith Visualization Network | General |
| `GET` | `/api/hadith/search` | Search Hadith | General |
| `GET` | `/api/hadith/search/en` | Search Hadith English | General |
| `GET` | `/api/hadith/{hadith_id}` | Get Hadith | General |
| `GET` | `/api/hadith/{hadith_id}/commentaries` | Get Hadith Commentaries | General |
| `GET` | `/api/hadith/{hadith_id}/commentary` | Get Hadith Commentaries | General |
| `GET` | `/api/hadith/{hadith_id}/crosswalk` | Get Hadith Crosswalk | General |
| `GET` | `/api/hadith/{hadith_id}/grades` | Get Hadith Grades | General |
| `GET` | `/api/hadith/{hadith_id}/group` | Get Hadith Group | General |
| `GET` | `/api/hadith/{hadith_id}/isnad` | Get Hadith Isnad | General |
| `GET` | `/api/hadith/{hadith_id}/numbering` | Get Hadith Numbering | General |
| `GET` | `/api/hadith/{hadith_id}/references` | Get Hadith Crosswalk | General |
| `GET` | `/api/hadith/{hadith_id}/sanad` | Get Hadith Isnad | General |
| `GET` | `/api/hadith/{hadith_id}/topics` | Get Hadith Topics | General |
| `GET` | `/api/hadith/{hadith_id}/translation` | Get Hadith Translations Endpoint | General |
| `GET` | `/api/hadith/{hadith_id}/translations` | Get Hadith Translations Endpoint | General |
| `GET` | `/api/health` | Health | General |
| `GET` | `/api/isnad/network` | Get Isnad Network | General |
| `GET` | `/api/isnad/network/diagnostics` | Isnad Network Diagnostics | General |
| `GET` | `/api/narrator/identity/search` | Search Narrator Identity | General |
| `GET` | `/api/narrator/{rawi_id}` | Get Narrator | General |
| `GET` | `/api/narrator/{rawi_id}/aliases` | Get Narrator Aliases Endpoint | General |
| `GET` | `/api/narrator/{rawi_id}/aqwal` | Get Narrator Aqwal | General |
| `GET` | `/api/narrator/{rawi_id}/identity` | Get Narrator Identity | General |
| `GET` | `/api/narrator/{rawi_id}/identity-candidates` | Get Narrator Identity Candidates | General |
| `GET` | `/api/narrator/{rawi_id}/relations` | Get Narrator Relations | General |
| `GET` | `/api/narrators` | List Narrators | General |
| `GET` | `/api/narrators/identity/search` | Search Narrator Identity | General |
| `GET` | `/api/narrators/{rawi_id}/aliases` | Get Narrator Aliases Endpoint | General |
| `GET` | `/api/narrators/{rawi_id}/identity` | Get Narrator Identity | General |
| `GET` | `/api/narrators/{rawi_id}/identity-candidates` | Get Narrator Identity Candidates | General |
| `GET` | `/api/narrators/{rawi_id}/relations` | Get Narrator Relations | General |
| `GET` | `/api/numbering/resolve` | Resolve Numbering Endpoint | General |
| `GET` | `/api/numbering/schemes` | List Numbering Schemes | General |
| `GET` | `/api/search-by-number` | Resolve Numbering Endpoint | General |
| `GET` | `/api/search/hybrid` | Search Hybrid Endpoint | General |
| `GET` | `/api/search/semantic` | Search Semantic Endpoint | General |
| `GET` | `/api/stats` | Stats | General |
| `GET` | `/api/translation-coverage` | Translation Coverage | General |
| `GET` | `/books/{book_id}/hadith/by-number/{hadith_number}` | Get Book Hadith By Number | General |
| `GET` | `/books/{book_id}/hadith/{hadith_number}` | Get Book Hadith By Number | General |
| `GET` | `/books/{book_id}/hadiths/by-number/{hadith_number}` | Get Book Hadith By Number | General |
| `GET` | `/books/{book_id}/numbering-options` | Get Book Numbering Options | General |
| `GET` | `/books/{book_id}/resolve-number` | Resolve Book Number Endpoint | General |
| `GET` | `/hadith/{hadith_id}/commentaries` | Get Hadith Commentaries | General |
| `GET` | `/hadith/{hadith_id}/commentary` | Get Hadith Commentaries | General |
| `GET` | `/narrator/{rawi_id}/aqwal` | Get Narrator Aqwal | General |
| `GET` | `/search-by-number` | Resolve Numbering Endpoint | General |
| `GET` | `/api/workspace/citation` | Generate Citation | Research Workspace |
| `DELETE` | `/api/workspace/claims/{claim_id}` | Delete Claim | Research Workspace |
| `PATCH` | `/api/workspace/claims/{claim_id}` | Update Claim | Research Workspace |
| `POST` | `/api/workspace/claims/{claim_id}/links` | Link Evidence To Claim | Research Workspace |
| `DELETE` | `/api/workspace/claims/{claim_id}/links/{evidence_item_id}` | Unlink Evidence From Claim | Research Workspace |
| `POST` | `/api/workspace/compare` | Compare Evidence Records | Research Workspace |
| `GET` | `/api/workspace/dashboard` | Get Research Dashboard | Research Workspace |
| `GET` | `/api/workspace/evidence/resolve` | Resolve Evidence Reference | Research Workspace |
| `DELETE` | `/api/workspace/evidence/{evidence_id}` | Delete Evidence Item | Research Workspace |
| `PATCH` | `/api/workspace/evidence/{evidence_id}` | Update Evidence Item | Research Workspace |
| `DELETE` | `/api/workspace/notes/{note_id}` | Delete Note | Research Workspace |
| `PATCH` | `/api/workspace/notes/{note_id}` | Update Note | Research Workspace |
| `GET` | `/api/workspace/projects` | List Projects | Research Workspace |
| `POST` | `/api/workspace/projects` | Create Project | Research Workspace |
| `DELETE` | `/api/workspace/projects/{project_id}` | Delete Project | Research Workspace |
| `GET` | `/api/workspace/projects/{project_id}` | Get Project | Research Workspace |
| `PATCH` | `/api/workspace/projects/{project_id}` | Update Project | Research Workspace |
| `GET` | `/api/workspace/projects/{project_id}/claims` | List Project Claims | Research Workspace |
| `POST` | `/api/workspace/projects/{project_id}/claims` | Create Claim | Research Workspace |
| `GET` | `/api/workspace/projects/{project_id}/evidence` | List Project Evidence | Research Workspace |
| `POST` | `/api/workspace/projects/{project_id}/evidence` | Add Evidence Item | Research Workspace |
| `POST` | `/api/workspace/projects/{project_id}/export` | Export Research Dossier | Research Workspace |
| `GET` | `/api/workspace/projects/{project_id}/notes` | List Project Notes | Research Workspace |
| `POST` | `/api/workspace/projects/{project_id}/notes` | Create Note | Research Workspace |
| `GET` | `/api/workspace/search` | Search Workspace | Research Workspace |

---

## 2. Detailed Endpoint Specifications


### Category: Ask Mīzān

#### `POST` `/api/ask`
**Summary:** Ask Hadith Query

**Request Body:** `application/json` (Schema: `AskRequest`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/ask/conversations/{conversation_id}`
**Summary:** Get Conversation

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `conversation_id` | path | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/ask/feedback`
**Summary:** Submit Feedback

**Request Body:** `application/json` (Schema: `FeedbackRequest`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/ask/health`
**Summary:** Ask Health

**Responses:**
- **HTTP 200:** Successful Response

---

#### `POST` `/api/ask/stream`
**Summary:** Ask Hadith Query Stream

**Request Body:** `application/json` (Schema: `AskRequest`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---


### Category: General

#### `GET` `/api/annotations`
**Summary:** Get Scholarly Annotations

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | query | No | `any` |  |
| `rawi_id` | query | No | `any` |  |
| `sanad_id` | query | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/annotations`
**Summary:** Create Scholarly Annotation

**Request Body:** `application/json` (Schema: `AnnotationCreate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books`
**Summary:** Get Books

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/books/{book_id}`
**Summary:** Get Book

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/hadith/by-number/{hadith_number}`
**Summary:** Get Book Hadith By Number

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `hadith_number` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/hadith/{hadith_number}`
**Summary:** Get Book Hadith By Number

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `hadith_number` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/hadiths`
**Summary:** Get Book Hadiths

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/hadiths/by-number/{hadith_number}`
**Summary:** Get Book Hadith By Number

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `hadith_number` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/hadiths/search`
**Summary:** Search Book Hadiths

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `q` | query | Yes | `string` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/numbering-options`
**Summary:** Get Book Numbering Options

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/resolve-number`
**Summary:** Resolve Book Number Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `scheme` | query | Yes | `string` |  |
| `number` | query | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/search`
**Summary:** Search Book Hadiths

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `q` | query | Yes | `string` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/books/{book_id}/search/en`
**Summary:** Search Book English

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `q` | query | Yes | `string` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/diagnostics/db-lifecycle`
**Summary:** Get Db Lifecycle Diagnostics

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/diagnostics/hybrid-shadow`
**Summary:** Get Hybrid Shadow Diagnostics

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/english-search/coverage`
**Summary:** English Search Coverage

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/hadith-visualization/hadith/{hadith_id}`
**Summary:** Get Hadith Visualization Detail

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith-visualization/network`
**Summary:** Get Hadith Visualization Network

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | query | No | `any` |  |
| `hadith_number` | query | No | `any` |  |
| `hadith_id` | query | No | `any` |  |
| `depth` | query | No | `integer` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/search`
**Summary:** Search Hadith

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | Yes | `string` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/search/en`
**Summary:** Search Hadith English

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | Yes | `string` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}`
**Summary:** Get Hadith

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/commentaries`
**Summary:** Get Hadith Commentaries

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/commentary`
**Summary:** Get Hadith Commentaries

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/crosswalk`
**Summary:** Get Hadith Crosswalk

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/grades`
**Summary:** Get Hadith Grades

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/group`
**Summary:** Get Hadith Group

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/isnad`
**Summary:** Get Hadith Isnad

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/numbering`
**Summary:** Get Hadith Numbering

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/references`
**Summary:** Get Hadith Crosswalk

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/sanad`
**Summary:** Get Hadith Isnad

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/topics`
**Summary:** Get Hadith Topics

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/translation`
**Summary:** Get Hadith Translations Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/hadith/{hadith_id}/translations`
**Summary:** Get Hadith Translations Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/health`
**Summary:** Health

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/isnad/network`
**Summary:** Get Isnad Network

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | query | No | `any` |  |
| `rawi_id` | query | No | `any` |  |
| `min_weight` | query | No | `integer` |  |
| `limit` | query | No | `integer` |  |
| `resolve_identity` | query | No | `boolean` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/isnad/network/diagnostics`
**Summary:** Isnad Network Diagnostics

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/narrator/identity/search`
**Summary:** Search Narrator Identity

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | Yes | `string` | Search by name, transliteration, or classical alias |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrator/{rawi_id}`
**Summary:** Get Narrator

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrator/{rawi_id}/aliases`
**Summary:** Get Narrator Aliases Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrator/{rawi_id}/aqwal`
**Summary:** Get Narrator Aqwal

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrator/{rawi_id}/identity`
**Summary:** Get Narrator Identity

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrator/{rawi_id}/identity-candidates`
**Summary:** Get Narrator Identity Candidates

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrator/{rawi_id}/relations`
**Summary:** Get Narrator Relations

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrators`
**Summary:** List Narrators

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | No | `string` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrators/identity/search`
**Summary:** Search Narrator Identity

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | Yes | `string` | Search by name, transliteration, or classical alias |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrators/{rawi_id}/aliases`
**Summary:** Get Narrator Aliases Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrators/{rawi_id}/identity`
**Summary:** Get Narrator Identity

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrators/{rawi_id}/identity-candidates`
**Summary:** Get Narrator Identity Candidates

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/narrators/{rawi_id}/relations`
**Summary:** Get Narrator Relations

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/numbering/resolve`
**Summary:** Resolve Numbering Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `collection` | query | Yes | `string` |  |
| `scheme` | query | No | `any` |  |
| `edition` | query | No | `any` |  |
| `number` | query | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/numbering/schemes`
**Summary:** List Numbering Schemes

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/search-by-number`
**Summary:** Resolve Numbering Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `collection` | query | Yes | `string` |  |
| `scheme` | query | No | `any` |  |
| `edition` | query | No | `any` |  |
| `number` | query | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/search/hybrid`
**Summary:** Search Hybrid Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | Yes | `string` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/search/semantic`
**Summary:** Search Semantic Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | Yes | `string` |  |
| `limit` | query | No | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/stats`
**Summary:** Stats

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/api/translation-coverage`
**Summary:** Translation Coverage

**Responses:**
- **HTTP 200:** Successful Response

---

#### `GET` `/books/{book_id}/hadith/by-number/{hadith_number}`
**Summary:** Get Book Hadith By Number

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `hadith_number` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/books/{book_id}/hadith/{hadith_number}`
**Summary:** Get Book Hadith By Number

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `hadith_number` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/books/{book_id}/hadiths/by-number/{hadith_number}`
**Summary:** Get Book Hadith By Number

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `hadith_number` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/books/{book_id}/numbering-options`
**Summary:** Get Book Numbering Options

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/books/{book_id}/resolve-number`
**Summary:** Resolve Book Number Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | path | Yes | `integer` |  |
| `scheme` | query | Yes | `string` |  |
| `number` | query | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/hadith/{hadith_id}/commentaries`
**Summary:** Get Hadith Commentaries

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/hadith/{hadith_id}/commentary`
**Summary:** Get Hadith Commentaries

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hadith_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/narrator/{rawi_id}/aqwal`
**Summary:** Get Narrator Aqwal

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `rawi_id` | path | Yes | `integer` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/search-by-number`
**Summary:** Resolve Numbering Endpoint

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `collection` | query | Yes | `string` |  |
| `scheme` | query | No | `any` |  |
| `edition` | query | No | `any` |  |
| `number` | query | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---


### Category: Research Workspace

#### `GET` `/api/workspace/citation`
**Summary:** Generate Citation

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `entity_type` | query | Yes | `string` |  |
| `source_id` | query | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `DELETE` `/api/workspace/claims/{claim_id}`
**Summary:** Delete Claim

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `claim_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `PATCH` `/api/workspace/claims/{claim_id}`
**Summary:** Update Claim

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `claim_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `ClaimUpdate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/workspace/claims/{claim_id}/links`
**Summary:** Link Evidence To Claim

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `claim_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `ClaimEvidenceLinkCreate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `DELETE` `/api/workspace/claims/{claim_id}/links/{evidence_item_id}`
**Summary:** Unlink Evidence From Claim

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `claim_id` | path | Yes | `string` |  |
| `evidence_item_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/workspace/compare`
**Summary:** Compare Evidence Records

**Request Body:** `application/json` (Schema: `ComparisonRequest`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/dashboard`
**Summary:** Get Research Dashboard

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/evidence/resolve`
**Summary:** Resolve Evidence Reference

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `entity_type` | query | Yes | `string` |  |
| `source_id` | query | Yes | `string` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `DELETE` `/api/workspace/evidence/{evidence_id}`
**Summary:** Delete Evidence Item

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `evidence_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `PATCH` `/api/workspace/evidence/{evidence_id}`
**Summary:** Update Evidence Item

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `evidence_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `EvidenceItemUpdate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `DELETE` `/api/workspace/notes/{note_id}`
**Summary:** Delete Note

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `note_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `PATCH` `/api/workspace/notes/{note_id}`
**Summary:** Update Note

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `note_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `NoteUpdate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/projects`
**Summary:** List Projects

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `status` | query | No | `any` |  |
| `archived` | query | No | `any` |  |
| `search` | query | No | `any` |  |
| `limit` | query | No | `integer` |  |
| `offset` | query | No | `integer` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/workspace/projects`
**Summary:** Create Project

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `ProjectCreate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `DELETE` `/api/workspace/projects/{project_id}`
**Summary:** Delete Project

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `confirm` | query | No | `boolean` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/projects/{project_id}`
**Summary:** Get Project

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `PATCH` `/api/workspace/projects/{project_id}`
**Summary:** Update Project

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `ProjectUpdate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/projects/{project_id}/claims`
**Summary:** List Project Claims

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/workspace/projects/{project_id}/claims`
**Summary:** Create Claim

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `ClaimCreate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/projects/{project_id}/evidence`
**Summary:** List Project Evidence

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `entity_type` | query | No | `any` |  |
| `role` | query | No | `any` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/workspace/projects/{project_id}/evidence`
**Summary:** Add Evidence Item

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `EvidenceItemCreate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/workspace/projects/{project_id}/export`
**Summary:** Export Research Dossier

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `DossierExportRequest`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/projects/{project_id}/notes`
**Summary:** List Project Notes

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `evidence_id` | query | No | `any` |  |
| `status` | query | No | `any` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `POST` `/api/workspace/projects/{project_id}/notes`
**Summary:** Create Note

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `project_id` | path | Yes | `string` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Request Body:** `application/json` (Schema: `NoteCreate`)

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---

#### `GET` `/api/workspace/search`
**Summary:** Search Workspace

**Parameters:**
| Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | query | Yes | `string` |  |
| `project_id` | query | No | `any` |  |
| `X-Researcher-Id` | header | No | `any` |  |

**Responses:**
- **HTTP 200:** Successful Response
- **HTTP 422:** Validation Error

---
