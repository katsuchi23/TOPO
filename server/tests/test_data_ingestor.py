import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_ingestion.json_ingestor import JSONIngestor
from data_ingestion.csv_ingestor import CSVIngestor
from data_ingestion.pdf_ingestor import PDFIngestor
from data_ingestion.pptx_ingestor import PPTXIngestor


def test_json_ingestor():
    ingestor = JSONIngestor('datasets/dataset1.json')
    data = ingestor.ingest()
    assert len(data['companies']) == 2
    assert data['companies'][1]['revenue'] == 0  # Test null revenue handling
    assert data['companies'][0]['employees'][7]['hired_date'] == 'Unknown'

def test_csv_ingestor():
    ingestor = CSVIngestor('datasets/dataset2.csv')
    data = ingestor.ingest()
    assert len(data) == 100
    assert isinstance(data[0]['Revenue'], float)

def test_pdf_ingestor():
    ingestor = PDFIngestor('datasets/dataset3.pdf')
    data = ingestor.ingest()
    assert len(data) == 10
    assert data[0]['Revenue (in $)'] == 2100000.0

def test_pptx_ingestor():
    ingestor = PPTXIngestor('datasets/dataset4.pptx')
    data = ingestor.ingest()
    assert data['total_revenue'] == 10400000.0
    assert data['total_memberships'] == 1520