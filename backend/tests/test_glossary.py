import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.glossary import GlossaryCategory, GlossaryTerm
from app.services import auth_service
from tests.conftest import TestSessionLocal


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _seed_glossary() -> None:
    async with TestSessionLocal() as db:
        renda_variavel = GlossaryCategory(slug="renda-variavel", name="Renda Variável", sort_order=1)
        renda_fixa = GlossaryCategory(slug="renda-fixa", name="Renda Fixa", sort_order=2)
        db.add_all([renda_variavel, renda_fixa])
        await db.flush()

        db.add_all(
            [
                GlossaryTerm(
                    category_id=renda_variavel.id,
                    slug="acao",
                    term="Ação",
                    short_definition="Menor parcela do capital social de uma empresa.",
                    full_explanation="Ao comprar uma ação você se torna sócio da empresa.",
                    example="Comprar PETR4.",
                ),
                GlossaryTerm(
                    category_id=renda_fixa.id,
                    slug="tesouro-selic",
                    term="Tesouro Selic",
                    short_definition="Título público pós-fixado que acompanha a Selic.",
                    full_explanation="Considerado o investimento mais conservador do mercado.",
                    example=None,
                ),
                GlossaryTerm(
                    category_id=renda_fixa.id,
                    slug="cdb",
                    term="CDB",
                    short_definition="Certificado de Depósito Bancário.",
                    full_explanation="Título de renda fixa emitido por bancos.",
                    example=None,
                ),
            ]
        )
        await db.commit()


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    async with TestSessionLocal() as db:
        await auth_service.register_user(db, "aprendiz@example.com", "senha12345", "Investidor")

    login = await client.post(
        "/api/v1/auth/login", json={"email": "aprendiz@example.com", "password": "senha12345"}
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def test_glossary_requires_authentication(client: AsyncClient):
    response = await client.get("/api/v1/glossary/categories")
    assert response.status_code == 401


async def test_list_categories_and_terms(client: AsyncClient):
    await _seed_glossary()
    headers = await _auth_headers(client)

    categories_response = await client.get("/api/v1/glossary/categories", headers=headers)
    assert categories_response.status_code == 200
    categories = categories_response.json()
    assert [c["slug"] for c in categories] == ["renda-variavel", "renda-fixa"]

    terms_response = await client.get("/api/v1/glossary/terms", headers=headers)
    assert terms_response.status_code == 200
    assert len(terms_response.json()) == 3

    filtered_response = await client.get(
        "/api/v1/glossary/terms", params={"category": "renda-fixa"}, headers=headers
    )
    filtered_terms = filtered_response.json()
    assert len(filtered_terms) == 2
    assert all(term["category"]["slug"] == "renda-fixa" for term in filtered_terms)

    search_response = await client.get(
        "/api/v1/glossary/terms", params={"q": "Tesouro"}, headers=headers
    )
    search_terms = search_response.json()
    assert len(search_terms) == 1
    assert search_terms[0]["term"] == "Tesouro Selic"


async def test_get_term_detail_and_404(client: AsyncClient):
    await _seed_glossary()
    headers = await _auth_headers(client)

    detail_response = await client.get("/api/v1/glossary/terms/acao", headers=headers)
    assert detail_response.status_code == 200
    body = detail_response.json()
    assert body["term"] == "Ação"
    assert body["full_explanation"]

    missing_response = await client.get("/api/v1/glossary/terms/inexistente", headers=headers)
    assert missing_response.status_code == 404
