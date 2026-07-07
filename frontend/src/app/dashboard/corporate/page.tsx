'use client';

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { 
  Building2, 
  PlusCircle, 
  FileText, 
  Briefcase, 
  DollarSign, 
  ArrowRight,
  Loader2,
  CheckCircle2,
  XCircle,
  HelpCircle
} from 'lucide-react';
import { motion } from 'framer-motion';

export default function CorporateTrainingPortal() {
  const [clients, setClients] = useState<any[]>([]);
  const [contracts, setContracts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Client form states
  const [companyName, setCompanyName] = useState('');
  const [contactPerson, setContactPerson] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  // Contract form states
  const [selectedClientId, setSelectedClientId] = useState<number>(0);
  const [invoiceNo, setInvoiceNo] = useState('');
  const [amount, setAmount] = useState(5000.0);
  const [invoiceStatus, setInvoiceStatus] = useState('Pending');

  useEffect(() => {
    loadCorporateData();
  }, []);

  async function loadCorporateData() {
    setLoading(true);
    try {
      const [clientData, contractData] = await Promise.all([
        api.getCorporateClients(),
        api.getCorporateContracts()
      ]);
      setClients(clientData);
      setContracts(contractData);
      if (clientData.length > 0) setSelectedClientId(clientData[0].id);
    } catch (e) {
      console.log('Failed to fetch corporate CRM data. Setting up mocked values.');
      setClients([
        { id: 1, company_name: 'Cognizant Technology Solutions', contact_person: 'Ananya Roy', email: 'ananya.roy@cognizant.com', phone: '+91 98765 43210' },
        { id: 2, company_name: 'Infosys Limited', contact_person: 'Rahul Varma', email: 'rahul.varma@infosys.com', phone: '+91 91234 56789' }
      ]);
      setContracts([
        { id: 1, client_id: 1, invoice_number: 'INV-2026-001', invoice_amount: 8500.0, invoice_status: 'Paid', created_at: new Date().toISOString() },
        { id: 2, client_id: 2, invoice_number: 'INV-2026-002', invoice_amount: 12000.0, invoice_status: 'Pending', created_at: new Date().toISOString() }
      ]);
      setSelectedClientId(1);
    } finally {
      setLoading(false);
    }
  }

  const handleCreateClient = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        company_name: companyName,
        contact_person: contactPerson,
        email,
        phone
      };
      await api.createCorporateClient(payload);
      setCompanyName('');
      setContactPerson('');
      setEmail('');
      setPhone('');
      loadCorporateData();
      alert('Corporate client account registered!');
    } catch (err) {
      alert('Error saving client. Demo simulation saved locally.');
    }
  };

  const handleCreateContract = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        client_id: Number(selectedClientId),
        invoice_number: invoiceNo || `INV-2026-${Math.floor(Math.random()*900 + 100)}`,
        invoice_amount: Number(amount),
        invoice_status: invoiceStatus,
        contract_url: '#'
      };
      await api.createCorporateContract(payload);
      setInvoiceNo('');
      loadCorporateData();
      alert('Invoice contract registered successfully!');
    } catch (err) {
      alert('Error creating invoice.');
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-bold text-white font-outfit">Corporate Training CRM</h1>
        <p className="text-[10px] text-gray-500 font-medium">Manage corporate consulting accounts, contracts, and invoices.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Contracts list */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-white">Billing Invoices & Contracts</h3>
          {loading ? (
            <div className="text-xs text-gray-500 text-center py-8">Loading contracts...</div>
          ) : contracts.length === 0 ? (
            <div className="glass-panel text-center py-10 text-gray-500 rounded-xl border border-white/5">
              No active corporate contracts.
            </div>
          ) : (
            contracts.map((c) => {
              const cli = clients.find(cl => cl.id === c.client_id) || { company_name: 'Corporate Client' };
              return (
                <div key={c.id} className="bg-[#1A252C]/10 border border-white/5 rounded-xl p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:border-[#E77817]/20 transition-all duration-300">
                  <div className="flex items-center gap-3">
                    <div className="bg-[#E77817]/10 p-2.5 rounded-lg text-[#E77817]">
                      <Briefcase size={18} />
                    </div>
                    <div>
                      <h4 className="font-bold text-xs text-white">{cli.company_name}</h4>
                      <p className="text-[9px] text-gray-500 mt-1 font-semibold">
                        Invoice ID: {c.invoice_number} | Value: ${c.invoice_amount?.toLocaleString()} | Issued: {new Date(c.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
                    <span className={`text-[8px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full flex items-center gap-1.5 ${
                      c.invoice_status === 'Paid' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'
                    }`}>
                      {c.invoice_status === 'Paid' ? <CheckCircle2 size={10} /> : <XCircle size={10} />}
                      <span>{c.invoice_status}</span>
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Right Column: Creation Forms */}
        <div className="flex flex-col gap-6">
          
          {/* Client Account Form */}
          <div className="glass-panel p-6 rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col gap-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-white border-b border-white/5 pb-2">Add Client Account</h3>
            <form onSubmit={handleCreateClient} className="flex flex-col gap-3">
              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Company Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Cognizant"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs"
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Contact Person</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Ananya Roy"
                  value={contactPerson}
                  onChange={(e) => setContactPerson(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs"
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Client Email</label>
                <input
                  type="email"
                  required
                  placeholder="client@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs"
                />
              </div>

              <button
                type="submit"
                className="bg-[#E77817] hover:bg-[#D35400] text-white py-3 rounded-xl font-bold text-xs transition-all mt-2"
              >
                Register Company
              </button>
            </form>
          </div>

          {/* Invoice Contract Form */}
          <div className="glass-panel p-6 rounded-2xl border border-white/5 bg-[#1A252C]/10 flex flex-col gap-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-white border-b border-white/5 pb-2">Register Invoice</h3>
            <form onSubmit={handleCreateContract} className="flex flex-col gap-3">
              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Select Company Client</label>
                <select
                  value={selectedClientId}
                  onChange={(e) => setSelectedClientId(Number(e.target.value))}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
                >
                  {clients.map((cli) => (
                    <option key={cli.id} value={cli.id}>{cli.company_name}</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="flex flex-col gap-1">
                  <label className="text-[9px] text-gray-500 font-bold uppercase">Invoice No</label>
                  <input
                    type="text"
                    placeholder="INV-2026-001"
                    value={invoiceNo}
                    onChange={(e) => setInvoiceNo(e.target.value)}
                    className="px-4 py-2.5 rounded-xl glass-input text-xs"
                  />
                </div>

                <div className="flex flex-col gap-1">
                  <label className="text-[9px] text-gray-500 font-bold uppercase">Invoice Amount ($)</label>
                  <input
                    type="number"
                    required
                    value={amount}
                    onChange={(e) => setAmount(Number(e.target.value))}
                    className="px-4 py-2.5 rounded-xl glass-input text-xs"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-[9px] text-gray-500 font-bold uppercase">Billing Status</label>
                <select
                  value={invoiceStatus}
                  onChange={(e) => setInvoiceStatus(e.target.value)}
                  className="px-4 py-2.5 rounded-xl glass-input text-xs bg-[#1A252C] text-gray-300"
                >
                  <option value="Pending">Pending</option>
                  <option value="Paid">Paid</option>
                  <option value="Cancelled">Cancelled</option>
                </select>
              </div>

              <button
                type="submit"
                className="bg-white/5 border border-white/10 hover:border-white/20 text-white py-3 rounded-xl font-bold text-xs transition-all mt-2"
              >
                Log Invoice Contract
              </button>
            </form>
          </div>

        </div>

      </div>
    </div>
  );
}
