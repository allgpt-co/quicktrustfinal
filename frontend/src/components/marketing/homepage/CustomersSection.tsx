import React from 'react';

export default function CustomersSection() {
  const companies = ['HealthTech Inc.', 'FinSecure', 'CloudSaaS', 'DataVault', 'MedFlow', 'SecurePay'];

  return React.createElement(
    'section',
    { className: 'py-12 sm:py-16 lg:py-24 bg-slate-900' },
    React.createElement(
      'div',
      { className: 'max-w-7xl mx-auto px-4 sm:px-6' },
      React.createElement(
        'div',
        { className: 'text-center mb-12 sm:mb-16' },
        React.createElement('h2', {
          className: 'font-display text-2xl sm:text-3xl lg:text-4xl font-bold text-slate-50 mb-4'
        }, 'Our Customers')
      )
    )
  );
}
