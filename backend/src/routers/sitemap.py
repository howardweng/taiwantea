from fastapi import APIRouter
from fastapi.responses import Response
from datetime import datetime
from ..models.product import ProductModel

router = APIRouter(tags=["sitemap"])

@router.get("/sitemap.xml")
async def generate_sitemap():
    """
    動態生成 sitemap.xml
    包含所有上架產品頁面
    """
    try:
        # 取得所有上架產品
        products = await ProductModel.get_all(in_stock_only=True)

        # 生成 XML
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        # 首頁
        xml_content += '  <url>\n'
        xml_content += '    <loc>https://taiwantea.frrut.com/</loc>\n'
        xml_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        xml_content += '    <changefreq>daily</changefreq>\n'
        xml_content += '    <priority>1.0</priority>\n'
        xml_content += '  </url>\n'

        # 產品頁面
        for product in products:
            xml_content += '  <url>\n'
            xml_content += f'    <loc>https://taiwantea.frrut.com/products/{product["_id"]}</loc>\n'
            xml_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            xml_content += '    <changefreq>weekly</changefreq>\n'
            xml_content += '    <priority>0.8</priority>\n'
            xml_content += '  </url>\n'

        xml_content += '</urlset>'

        return Response(content=xml_content, media_type="application/xml")

    except Exception as e:
        # 如果出錯，返回基本的 sitemap
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml_content += '  <url>\n'
        xml_content += '    <loc>https://taiwantea.frrut.com/</loc>\n'
        xml_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        xml_content += '    <changefreq>daily</changefreq>\n'
        xml_content += '    <priority>1.0</priority>\n'
        xml_content += '  </url>\n'
        xml_content += '</urlset>'

        return Response(content=xml_content, media_type="application/xml")
